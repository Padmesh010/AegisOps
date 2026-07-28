import pytest
from typing import AsyncGenerator, List
from app.providers.ai.factory import ai_factory
from app.providers.ai.base import BaseProvider
from app.providers.ai.models import ModelRequest, ModelResponse, ModelMetadata, TokenUsage, ChatMessage
from app.providers.ai.manager import AIProviderManager
from app.core.exceptions import AIProviderError

# Create a mock provider class for test validation
class MockTestProvider(BaseProvider):
    def __init__(self, name: str, should_fail: bool = False, healthy: bool = True) -> None:
        super().__init__()
        self.name = name
        self.should_fail = should_fail
        self.healthy = healthy

    def get_name(self) -> str:
        return self.name

    async def generate_completion(self, req: ModelRequest) -> ModelResponse:
        if self.should_fail:
            raise AIProviderError("Mock service connection failure", provider=self.name)
        return ModelResponse(
            content=f"Mock response from {self.name}",
            model=req.model,
            usage=TokenUsage(total_tokens=10),
            latency_ms=50
        )

    async def generate_stream(self, req: ModelRequest) -> AsyncGenerator[ModelResponse, None]:
        yield await self.generate_completion(req)

    async def get_models(self) -> List[ModelMetadata]:
        return [ModelMetadata(name="mock-model")]

    async def health_check(self) -> bool:
        return self.healthy

@pytest.mark.anyio
async def test_ai_provider_factory_resolution() -> None:
    ai_factory.register_provider("mock-1", lambda: MockTestProvider("mock-1"))
    provider = ai_factory.get_provider("mock-1")
    assert provider.get_name() == "mock-1"

@pytest.mark.anyio
async def test_ai_manager_fallback_chain() -> None:
    # Setup two mock providers, the first one failing and the second one succeeding
    p1 = MockTestProvider("mock-fail", should_fail=True)
    p2 = MockTestProvider("mock-success")
    
    ai_factory.register_provider("mock-fail", lambda: p1)
    ai_factory.register_provider("mock-success", lambda: p2)
    
    manager = AIProviderManager(fallback_chain=["mock-fail", "mock-success"])
    req = ModelRequest(
        model="test-model",
        messages=[ChatMessage(role="user", content="Ping")]
    )
    
    response = await manager.generate_completion_with_fallback(req)
    assert response.content == "Mock response from mock-success"

@pytest.mark.anyio
async def test_ai_manager_complete_failure() -> None:
    p1 = MockTestProvider("mock-fail-1", should_fail=True)
    p2 = MockTestProvider("mock-fail-2", should_fail=True)
    
    ai_factory.register_provider("mock-fail-1", lambda: p1)
    ai_factory.register_provider("mock-fail-2", lambda: p2)
    
    manager = AIProviderManager(fallback_chain=["mock-fail-1", "mock-fail-2"])
    req = ModelRequest(
        model="test-model",
        messages=[ChatMessage(role="user", content="Ping")]
    )
    
    with pytest.raises(AIProviderError):
        await manager.generate_completion_with_fallback(req)
