from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.services.aiops.anomaly import anomaly_engine
from app.services.aiops.prediction import predictive_engine
from app.services.aiops.forecaster import forecast_engine
from app.services.aiops.health_scoring import health_scoring_engine

router = APIRouter()

@router.post("/anomaly/detect", response_model=dict)
async def trigger_anomaly_detection(
    metric_name: str,
    history: List[float],
    strategy: str = "zscore",
    user: Any = Depends(get_current_user)
) -> dict:
    if strategy == "isolation_forest":
        res = anomaly_engine.detect_isolation_forest(history)
    else:
        res = anomaly_engine.detect_zscore(history)
    return {"status": "success", "result": res}

@router.post("/predict/failure", response_model=dict)
async def predict_failure(
    target_id: str,
    metric_history: List[float],
    user: Any = Depends(get_current_user)
) -> dict:
    pred = await predictive_engine.predict_node_failure(target_id, metric_history)
    return {"id": str(pred.id), "failure_type": pred.failure_type, "probability": pred.probability}

@router.get("/health/scores", response_model=dict)
async def get_health_score(
    scope_type: str,
    scope_id: str,
    user: Any = Depends(get_current_user)
) -> dict:
    factors = {"cpu_spikes": 1.0, "slo_violations": 0.0, "vulnerabilities": 2.0}
    health = await health_scoring_engine.calculate_scope_health(scope_type, scope_id, factors)
    return {
        "scope_type": health.scope_type,
        "scope_id": health.scope_id,
        "health_score": health.health_score,
        "factors": health.breakdown_json
    }

from typing import Any
