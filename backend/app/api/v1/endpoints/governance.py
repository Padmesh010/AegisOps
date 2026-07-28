from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.services.governance.policy_engine import policy_evaluator_engine
from app.services.governance.compliance import compliance_framework_engine
from app.services.governance.audit import audit_logger

router = APIRouter()

@router.post("/policies/evaluate", response_model=dict)
async def evaluate_policy_rules(
    action_name: str,
    resource_id: str,
    parameters: dict,
    user: Any = Depends(get_current_user)
) -> dict:
    # Build active policies mocks
    active_policies = [
        {"rules": {"block_prod_scale_down": True}, "enforcement_mode": "enforce"}
    ]
    res = policy_evaluator_engine.evaluate_resource_action(action_name, resource_id, parameters, active_policies)
    
    # Audit log
    await audit_logger.log_audit_event(
        event_type="policy_evaluation",
        actor_id=str(user.id),
        action=action_name,
        target_id=resource_id,
        payload={"result": res}
    )
    
    return res

@router.get("/compliance/score", response_model=list[dict])
async def get_compliance_score(
    framework: str = "CIS",
    user: Any = Depends(get_current_user)
) -> list[dict]:
    findings = await compliance_framework_engine.run_compliance_assessment(framework)
    return [
        {
            "id": str(f.id),
            "rule_id": f.rule_id,
            "status": f.status,
            "target": f.target_resource_id,
            "severity": f.severity
        } for f in findings
    ]

from typing import Any
