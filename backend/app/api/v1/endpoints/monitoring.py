from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.monitoring import Node
from app.infrastructure.db.models.metric import DbAlertThreshold
from app.infrastructure.db.repositories.monitoring import NodeRepository, AlertThresholdRepository

router = APIRouter()

@router.get("/nodes", response_model=List[dict])
async def list_nodes(
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> List[dict]:
    node_repo = NodeRepository(db)
    nodes = await node_repo.get_multi(limit=50)
    return [
        {"id": str(n.id), "name": n.name, "status": n.status}
        for n in nodes
    ]

@router.post("/thresholds", status_code=201)
async def create_alert_threshold(
    metric_name: str,
    warning: float,
    critical: float,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    repo = AlertThresholdRepository(db)
    threshold = DbAlertThreshold(
        metric_name=metric_name,
        warning_limit=warning,
        critical_limit=critical
    )
    await repo.create(threshold)
    return {"status": "created", "metric": metric_name}

from typing import Any
