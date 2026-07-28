import logging
from typing import Dict, Any, List

logger = logging.getLogger("app.services.governance.policy_engine")

class PolicyEvaluationEngine:
    def evaluate_resource_action(
        self,
        action_name: str,
        resource_id: str,
        parameters: dict,
        active_policies: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate if SRE actions comply with organizational rules, supporting dry-runs."""
        violations = []
        enforced = True
        
        for policy in active_policies:
            rules = policy.get("rules", {})
            mode = policy.get("enforcement_mode", "audit")  # audit, warn, enforce
            
            # Policy Rule logic: if action is scale-down and resources have tag 'prod', enforce checks
            if action_name == "scale_down" and rules.get("block_prod_scale_down", False):
                tags = parameters.get("tags", {})
                if tags.get("env") == "prod":
                    violations.append(f"Policy Violation: Action {action_name} blocks prod scale-down.")
                    if mode == "enforce":
                        enforced = False
                        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "allowed_execution": enforced
        }

# Global engine instance
policy_evaluator_engine = PolicyEvaluationEngine()
