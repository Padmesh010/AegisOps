from fastapi import APIRouter, Depends
from typing import List
from app.api.dependencies import get_current_user, RequirePermission
from app.providers.ai.manager import ai_manager
from app.providers.ai.models import ModelRequest, ModelResponse, ProviderStatus, BenchmarkResult

router = APIRouter()

@router.get("/status", response_model=List[ProviderStatus])
async def get_providers_status(
    user: Any = Depends(get_current_user)
) -> List[ProviderStatus]:
    """Get active status and benchmark latency of all configured AI providers."""
    return await ai_manager.get_active_providers_status()

@router.post("/completions", response_model=ModelResponse)
async def generate_completion(
    req: ModelRequest,
    user: Any = Depends(RequirePermission("ai:completion"))
) -> ModelResponse:
    """Submit prompt context and generate a complete text completion."""
    return await ai_manager.generate_completion_with_fallback(req)

@router.post("/benchmark/{provider}/{model}", response_model=BenchmarkResult)
async def trigger_benchmark(
    provider: str,
    model: str,
    user: Any = Depends(RequirePermission("admin"))
) -> BenchmarkResult:
    """Run a latency and throughput benchmark test on a specific model."""
    return await ai_manager.run_benchmark(provider, model)

from typing import Any
