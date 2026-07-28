import pytest
import uuid
from app.services.agents.registry import agent_registry
from app.services.agents.safety import safety_limits
from app.services.agents.planner import goal_planner
from app.services.agents.approvals import agent_approvals

def test_registry_builtins():
    sre = agent_registry.get_agent("SREAgent")
    assert sre is not None
    assert "incident_investigation" in sre.get_capabilities()
    
    devops = agent_registry.get_agent("DevOpsAgent")
    assert devops is not None

def test_safety_limits():
    assert safety_limits.can_proceed(3, 10) is True
    assert safety_limits.can_proceed(10, 10) is False

@pytest.mark.asyncio
async def test_goal_decomposition_tasks():
    session_id = uuid.uuid4()
    tasks = await goal_planner.create_execution_plan(session_id, "investigate incident memory leaks")
    assert len(tasks) >= 1
    assert any(t.assigned_agent in ["SREAgent", "KubernetesAgent"] for t in tasks)

@pytest.mark.asyncio
async def test_action_approvals_tickets():
    session_id = uuid.uuid4()
    approval = await agent_approvals.request_action_approval(
        session_id, "terminate_node", "i-0123456789abcdef0", {"grace_sec": 30}
    )
    assert approval.risk_score == 90.0
    assert approval.status == "pending"
    
    success = await agent_approvals.cast_approval_decision(approval.id, True, "Approved by admin")
    assert success is True
