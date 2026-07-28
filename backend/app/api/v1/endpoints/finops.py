from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.finops import DbBudget
from app.services.finops.collector import cost_collector
from app.services.finops.analytics import cost_analytics
from app.services.finops.rightsizing import rightsizing_engine

router = APIRouter()

@router.post("/sync/{account_id}", response_model=dict)
async def sync_costs(
    account_id: str,
    user: Any = Depends(get_current_user)
) -> dict:
    records = await cost_collector.synchronize_aws_billing(account_id)
    return {"status": "synchronized", "records_count": len(records)}

@router.get("/costs/summary", response_model=dict)
async def get_costs_summary(
    user: Any = Depends(get_current_user)
) -> dict:
    summary = await cost_analytics.aggregate_costs_by_service()
    return {"costs_by_service": summary}

@router.get("/rightsizing/recommendations", response_model=list[dict])
async def get_rightsizing_recommendations(
    user: Any = Depends(get_current_user)
) -> list[dict]:
    # Mock resources list
    resources = [
        {"id": "i-0123456789abcdef0", "cpu_avg": 2.5, "size": "t3.large"},
        {"id": "db-prod-postgres", "cpu_avg": 20.0, "size": "db.m5.large"}
    ]
    recs = rightsizing_engine.identify_rightsizing_options(resources)
    return recs

from typing import Any
