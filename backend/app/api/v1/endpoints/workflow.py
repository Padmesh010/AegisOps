from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.notification import DbWorkflowDefinition

router = APIRouter()

@router.post("", status_code=201)
async def create_automation_workflow(
    name: str,
    trigger_type: str,
    steps: dict,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    workflow = DbWorkflowDefinition(
        name=name,
        trigger_type=trigger_type,
        steps_definition=steps
    )
    db.add(workflow)
    await db.commit()
    return {"status": "created", "workflow_id": str(workflow.id)}

from typing import Any
