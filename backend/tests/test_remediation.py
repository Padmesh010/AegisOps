import pytest
from app.services.remediation.policy import policy_evaluator
from app.services.remediation.planner import remediation_planner

@pytest.mark.anyio
async def test_remediation_policy_evaluation() -> None:
    # Safe check default fallback: if no policies exist in DB, evaluate denies
    allowed = await policy_evaluator.is_action_allowed("clear_temp_files", "high")
    assert allowed is False

@pytest.mark.anyio
async def test_remediation_planner_steps() -> None:
    steps = remediation_planner.create_plan_steps("High CPU Utilization Alert")
    assert len(steps) == 2
    assert steps[0]["action"] == "clear_temp_files"
    assert steps[1]["action"] == "restart_service"
