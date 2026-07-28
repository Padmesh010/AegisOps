import logging
import time
from typing import List, Dict, Optional, AsyncGenerator
from app.providers.ai.interface import AIProvider
from app.providers.ai.factory import ai_factory
from app.providers.ai.models import ModelRequest, ModelResponse, ProviderStatus, BenchmarkResult
from app.core.config import get_settings
from app.core.exceptions import AIProviderError, AIRateLimitError, AIConnectionTimeout

logger = logging.getLogger("app.providers.ai.manager")
settings = get_settings()

class AIProviderManager:
    def __init__(self, fallback_chain: Optional[List[str]] = None) -> None:
        self.fallback_chain = fallback_chain or settings.AI_FALLBACK_CHAIN
        self.default_provider_name = self.fallback_chain[0] if self.fallback_chain else "ollama"

    def get_provider(self, name: Optional[str] = None) -> AIProvider:
        provider_name = name or self.default_provider_name
        return ai_factory.get_provider(provider_name)

    async def generate_completion_with_fallback(self, req: ModelRequest, preferred_provider: Optional[str] = None) -> ModelResponse:
        """Submit a prompt and fallback sequentially to the next provider if a failure is encountered."""
        providers_to_try = list(self.fallback_chain)
        
        # Insert preferred provider at the beginning of the chain if specified
        if preferred_provider:
            if preferred_provider in providers_to_try:
                providers_to_try.remove(preferred_provider)
            providers_to_try.insert(0, preferred_provider)

        last_error: Optional[Exception] = None
        
        for provider_name in providers_to_try:
            try:
                logger.info(f"Attempting completion using provider: {provider_name}")
                provider = self.get_provider(provider_name)
                # Ensure the provider is healthy before submitting execution
                is_healthy = await provider.health_check()
                if not is_healthy:
                    raise AIProviderError(f"Provider {provider_name} failed health check prior to execution", provider=provider_name)
                
                return await provider.generate_completion(req)
            except (AIProviderError, AIRateLimitError, AIConnectionTimeout) as err:
                logger.warn(f"Provider '{provider_name}' failed to process completion request. Attempting fallback. Error: {str(err)}")
                last_error = err
                continue
            except Exception as err:
                logger.error(f"Unexpected error in provider '{provider_name}': {str(err)}")
                last_error = err
                continue

        logger.error("All AI providers in fallback chain failed to generate completion.")
        if last_error:
            raise last_error
        raise AIProviderError("No AI providers available in the configured chain.", provider="manager")

    async def get_active_providers_status(self) -> List[ProviderStatus]:
        """Detect and return health metrics of all configured providers."""
        status_list = []
        for name in ["ollama", "openai"]:
            try:
                provider = self.get_provider(name)
                start_time = time.perf_counter()
                is_healthy = await provider.health_check()
                latency_ms = int((time.perf_counter() - start_time) * 1000) if is_healthy else 0
                
                models = []
                if is_healthy:
                    metadata = await provider.get_models()
                    models = [m.name for m in metadata]
                
                status_list.append(
                    ProviderStatus(
                        name=name,
                        is_active=is_healthy,
                        latency_ms=latency_ms,
                        available_models=models
                    )
                )
            except Exception as err:
                logger.debug(f"Failed to check health for provider '{name}': {str(err)}")
                status_list.append(
                    ProviderStatus(name=name, is_active=False, latency_ms=0, available_models=[])
                )
        return status_list

    async def run_benchmark(self, provider_name: str, model_name: str) -> BenchmarkResult:
        """Run a standard benchmark request to measure latency, throughput and success rate."""
        provider = self.get_provider(provider_name)
        from app.providers.ai.models import ChatMessage
        test_req = ModelRequest(
            model=model_name,
            messages=[ChatMessage(role="user", content="Respond with the single word 'Pong'")],
            temperature=0.0,
            max_tokens=5
        )
        
        start_time = time.perf_counter()
        try:
            response = await provider.generate_completion(test_req)
            elapsed = time.perf_counter() - start_time
            latency_ms = int(elapsed * 1000)
            
            # Simple word-based throughput estimate
            tokens_generated = len(response.content.split())
            tokens_per_sec = tokens_generated / elapsed if elapsed > 0 else 0.0
            
            return BenchmarkResult(
                provider=provider_name,
                model=model_name,
                latency_ms=latency_ms,
                tokens_per_second=tokens_per_sec,
                success=True
            )
        except Exception as err:
            logger.error(f"Benchmark failed for {provider_name}/{model_name}: {str(err)}")
            return BenchmarkResult(
                provider=provider_name,
                model=model_name,
                latency_ms=0,
                tokens_per_second=0.0,
                success=False,
                error_message=str(err)
            )

# Global manager instance
ai_manager = AIProviderManager()
