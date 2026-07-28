from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.agents import DbAgentSession
from app.services.agents.planner import goal_planner
from app.services.agents.executor import task_executor
from app.services.agents.approvals import agent_approvals

router = APIRouter()

@router.post("/goals", response_model=dict)
async def submit_agent_goal(
    goal: str,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    session_item = DbAgentSession(goal=goal, status="running", max_steps=10)
    db.add(session_item)
    await db.commit()
    
    # Decompose into tasks
    await goal_planner.create_execution_plan(session_item.id, goal)
    
    # Trigger background execution task
    import asyncio
    asyncio.create_task(task_executor.execute_session_tasks(session_item.id))
    
    return {"status": "accepted", "session_id": str(session_item.id)}

@router.post("/approvals/{approval_id}/decision", response_model=dict)
async def decide_approval_workflow(
    approval_id: str,
    approve: bool,
    reason: str = "",
    user: Any = Depends(get_current_user)
) -> dict:
    parsed_id = uuid.UUID(approval_id)
    success = await agent_approvals.cast_approval_decision(parsed_id, approve, reason)
    if not success:
        raise HTTPException(status_code=404, detail="Approval ticket not found.")
    return {"status": "success", "approved": approve}

from typing import Any
