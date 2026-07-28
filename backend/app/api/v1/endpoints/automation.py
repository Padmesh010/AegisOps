from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.automation import DbWorkflowDefinition
from app.services.automation.engine import workflow_execution_engine
from app.services.automation.ai_assistant import ai_workflow_assistant

router = APIRouter()

@router.post("/workflows", response_model=dict)
async def create_workflow_definition(
    name: str,
    trigger_type: str,
    dag_nodes: dict,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    wf = DbWorkflowDefinition(
        name=name,
        trigger_type=trigger_type,
        dag_nodes_json=dag_nodes,
        status="published"
    )
    db.add(wf)
    await db.commit()
    return {"status": "created", "workflow_id": str(wf.id)}

@router.post("/workflows/{workflow_id}/execute", response_model=dict)
async def execute_workflow(
    workflow_id: str,
    payload: dict,
    user: Any = Depends(get_current_user)
) -> dict:
    parsed_id = uuid.UUID(workflow_id)
    execution = await workflow_execution_engine.execute_workflow(parsed_id, payload)
    return {
        "execution_id": str(execution.id),
        "status": execution.status,
        "logs": execution.execution_logs
    }

@router.post("/workflows/ai-generate", response_model=dict)
async def ai_generate_workflow(
    prompt: str,
    user: Any = Depends(get_current_user)
) -> dict:
    dag_str = await ai_workflow_assistant.generate_workflow_dag(prompt)
    return {"generated_dag": dag_str}

from typing import Any
