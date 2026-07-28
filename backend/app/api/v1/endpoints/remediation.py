from fastapi import APIRouter, Depends, HTTPException
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.services.remediation.planner import remediation_planner
from app.services.remediation.executor import remediation_executor
from app.infrastructure.db.repositories.remediation import RemediationPlanRepository

router = APIRouter()

@router.post("/plans/{incident_id}", response_model=dict)
async def generate_healing_plan(
    incident_id: str,
    incident_title: str,
    user: Any = Depends(get_current_user)
) -> dict:
    parsed_id = uuid.UUID(incident_id)
    plan = await remediation_planner.generate_plan(parsed_id, incident_title)
    return {
        "plan_id": str(plan.id),
        "status": plan.status,
        "steps": plan.steps_data
    }

@router.post("/plans/{plan_id}/execute", response_model=dict)
async def trigger_plan_execution(
    plan_id: str,
    user: Any = Depends(get_current_user)
) -> dict:
    parsed_id = uuid.UUID(plan_id)
    success = await remediation_executor.execute_plan(parsed_id)
    return {"status": "executed" if success else "failed"}

from typing import Any
