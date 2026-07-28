import time
import httpx
import json
from typing import AsyncGenerator, List
from app.providers.ai.base import BaseProvider
from app.providers.ai.models import ModelRequest, ModelResponse, ModelMetadata, TokenUsage
from app.core.config import get_settings
from app.core.exceptions import AIProviderError, AIRateLimitError, AIConnectionTimeout

settings = get_settings()

class OpenAIProvider(BaseProvider):
    def get_name(self) -> str:
        return "openai"

    def _get_headers(self) -> dict:
        if not settings.OPENAI_API_KEY:
            raise AIProviderError("OpenAI API key is missing. Configure OPENAI_API_KEY in environment settings.", provider="openai")
        return {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

    async def generate_completion(self, req: ModelRequest) -> ModelResponse:
        start_time = time.perf_counter()
        headers = self._get_headers()
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "model": req.model,
                "messages": [{"role": m.role, "content": m.content} for m in req.messages],
                "temperature": req.temperature,
                "stream": False
            }
            if req.max_tokens:
                payload["max_tokens"] = req.max_tokens

            try:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                if response.status_code == 429:
                    raise AIRateLimitError(provider="openai")
                if response.status_code != 200:
                    raise AIProviderError(f"OpenAI server returned {response.status_code}: {response.text}", provider="openai")
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                usage_data = data.get("usage", {})
                usage = TokenUsage(
                    prompt_tokens=usage_data.get("prompt_tokens", 0),
                    completion_tokens=usage_data.get("completion_tokens", 0),
                    total_tokens=usage_data.get("total_tokens", 0)
                )
                
                # Estimate cost
                cost = (usage.prompt_tokens * 0.005 + usage.completion_tokens * 0.015) / 1000.0
                latency_ms = int((time.perf_counter() - start_time) * 1000)
                return ModelResponse(
                    content=content,
                    model=req.model,
                    usage=usage,
                    latency_ms=latency_ms,
                    finish_reason=data["choices"][0].get("finish_reason"),
                    cost_estimate=cost
                )
            except httpx.TimeoutException as err:
                raise AIConnectionTimeout(provider="openai", message=str(err))
            except Exception as err:
                if isinstance(err, (AIProviderError, AIRateLimitError, AIConnectionTimeout)):
                    raise err
                raise AIProviderError(f"OpenAI completion execution failed: {str(err)}", provider="openai")

    async def generate_stream(self, req: ModelRequest) -> AsyncGenerator[ModelResponse, None]:
        start_time = time.perf_counter()
        headers = self._get_headers()
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "model": req.model,
                "messages": [{"role": m.role, "content": m.content} for m in req.messages],
                "temperature": req.temperature,
                "stream": True
            }
            try:
                async with client.stream(
                    "POST",
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status_code == 429:
                        raise AIRateLimitError(provider="openai")
                    if response.status_code != 200:
                        raise AIProviderError(f"OpenAI stream initiation failed with code {response.status_code}", provider="openai")
                    
                    async for line in response.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        chunk = json.loads(data_str)
                        content = chunk["choices"][0]["delta"].get("content", "")
                        finish_reason = chunk["choices"][0].get("finish_reason")
                        
                        latency_ms = int((time.perf_counter() - start_time) * 1000)
                        yield ModelResponse(
                            content=content,
                            model=req.model,
                            usage=TokenUsage(),
                            latency_ms=latency_ms,
                            finish_reason=finish_reason
                        )
            except httpx.TimeoutException as err:
                raise AIConnectionTimeout(provider="openai", message=str(err))
            except Exception as err:
                if isinstance(err, (AIProviderError, AIRateLimitError, AIConnectionTimeout)):
                    raise err
                raise AIProviderError(f"OpenAI stream failure: {str(err)}", provider="openai")

    async def get_models(self) -> List[ModelMetadata]:
        # Static representation of enterprise compatible standard OpenAI models
        return [
            ModelMetadata(name="gpt-4o", context_length=128000, capabilities=["chat", "vision"], cost_per_1k_input=0.005, cost_per_1k_output=0.015),
            ModelMetadata(name="gpt-4-turbo", context_length=128000, capabilities=["chat"], cost_per_1k_input=0.01, cost_per_1k_output=0.03),
            ModelMetadata(name="gpt-3.5-turbo", context_length=16385, capabilities=["chat"], cost_per_1k_input=0.0005, cost_per_1k_output=0.0015)
        ]

    async def health_check(self) -> bool:
        if not settings.OPENAI_API_KEY:
            return False
        async with httpx.AsyncClient(timeout=3.0) as client:
            try:
                response = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
                )
                return response.status_code == 200
            except Exception:
                return False
