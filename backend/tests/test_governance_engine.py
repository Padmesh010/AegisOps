import pytest
import json
from app.services.governance.policy_engine import policy_evaluator_engine
from app.services.governance.audit import audit_logger

def test_policy_enforcement_rules():
    active_policies = [
        {"rules": {"block_prod_scale_down": True}, "enforcement_mode": "enforce"}
    ]
    
    # 1. Action scale_down on prod resource -> blocked
    res_prod = policy_evaluator_engine.evaluate_resource_action(
        "scale_down", "i-123", {"tags": {"env": "prod"}}, active_policies
    )
    assert res_prod["compliant"] is False
    assert res_prod["allowed_execution"] is False
    
    # 2. Action scale_down on dev resource -> allowed
    res_dev = policy_evaluator_engine.evaluate_resource_action(
        "scale_down", "i-456", {"tags": {"env": "dev"}}, active_policies
    )
    assert res_dev["compliant"] is True
    assert res_dev["allowed_execution"] is True

def test_audit_logs_signatures():
    payload = {"status": "success", "user": "admin"}
    h1 = audit_logger.calculate_event_hash("policy_eval", "user-1", "write", "target-2", payload)
    h2 = audit_logger.calculate_event_hash("policy_eval", "user-1", "write", "target-2", payload)
    
    assert h1 == h2
    assert len(h1) == 64  # SHA256 string length
