import time
import httpx
from typing import AsyncGenerator, List
from app.providers.ai.base import BaseProvider
from app.providers.ai.models import ModelRequest, ModelResponse, ModelMetadata, TokenUsage
from app.core.config import get_settings
from app.core.exceptions import AIProviderError, AIConnectionTimeout

settings = get_settings()

class OllamaProvider(BaseProvider):
    def get_name(self) -> str:
        return "ollama"

    async def generate_completion(self, req: ModelRequest) -> ModelResponse:
        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "model": req.model,
                "messages": [{"role": m.role, "content": m.content} for m in req.messages],
                "stream": False,
                "options": {
                    "temperature": req.temperature,
                }
            }
            if req.max_tokens:
                payload["options"]["num_predict"] = req.max_tokens # type: ignore

            try:
                response = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/chat",
                    json=payload
                )
                if response.status_code != 200:
                    raise AIProviderError(f"Ollama server returned {response.status_code}: {response.text}", provider="ollama")
                
                data = response.json()
                content = data["message"]["content"]
                
                # Estimate token counts
                prompt_tokens = len(str(req.messages)) // 4
                completion_tokens = len(content) // 4
                usage = TokenUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens
                )
                
                latency_ms = int((time.perf_counter() - start_time) * 1000)
                return ModelResponse(
                    content=content,
                    model=req.model,
                    usage=usage,
                    latency_ms=latency_ms,
                    cost_estimate=0.0
                )
            except httpx.TimeoutException as err:
                raise AIConnectionTimeout(provider="ollama", message=str(err))
            except Exception as err:
                if isinstance(err, (AIProviderError, AIConnectionTimeout)):
                    raise err
                raise AIProviderError(f"Ollama connection failed: {str(err)}", provider="ollama")

    async def generate_stream(self, req: ModelRequest) -> AsyncGenerator[ModelResponse, None]:
        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "model": req.model,
                "messages": [{"role": m.role, "content": m.content} for m in req.messages],
                "stream": True,
                "options": {
                    "temperature": req.temperature,
                }
            }
            try:
                async with client.stream("POST", f"{settings.OLLAMA_BASE_URL}/api/chat", json=payload) as response:
                    if response.status_code != 200:
                        raise AIProviderError(f"Ollama stream initiation failed with code {response.status_code}", provider="ollama")
                    
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        import json
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        done = chunk.get("done", False)
                        
                        latency_ms = int((time.perf_counter() - start_time) * 1000)
                        yield ModelResponse(
                            content=content,
                            model=req.model,
                            usage=TokenUsage(),
                            latency_ms=latency_ms,
                            finish_reason="stop" if done else None
                        )
            except httpx.TimeoutException as err:
                raise AIConnectionTimeout(provider="ollama", message=str(err))
            except Exception as err:
                raise AIProviderError(f"Ollama streaming failure: {str(err)}", provider="ollama")

    async def get_models(self) -> List[ModelMetadata]:
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
                if response.status_code != 200:
                    return []
                models = response.json().get("models", [])
                return [
                    ModelMetadata(
                        name=m["name"],
                        capabilities=["chat", "generate"],
                        cost_per_1k_input=0.0,
                        cost_per_1k_output=0.0
                    ) for m in models
                ]
            except Exception:
                return []

    async def health_check(self) -> bool:
        async with httpx.AsyncClient(timeout=3.0) as client:
            try:
                response = await client.get(f"{settings.OLLAMA_BASE_URL}/")
                return response.status_code == 200
            except Exception:
                return False
