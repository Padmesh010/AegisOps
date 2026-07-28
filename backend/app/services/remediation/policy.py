from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.remediation import RemediationPolicy

class PolicyEvaluator:
    async def is_action_allowed(self, action_name: str, risk_level: str) -> bool:
        """Validate if an automation action is allowed based on active remediation policies."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(RemediationPolicy).where(
                    RemediationPolicy.action_plugin == action_name,
                    RemediationPolicy.is_active == True
                )
            )
            policies = res.scalars().all()
            
            if not policies:
                # Default safety: Deny automation if no policy matches
                return False

            for policy in policies:
                # E.g. deny critical risk actions if the policy only allows low/medium
                if risk_level == "critical" and policy.risk_allowance != "critical":
                    return False
                if risk_level == "high" and policy.risk_allowance not in ["high", "critical"]:
                    return False
                    
            return True

# Global evaluator instance
policy_evaluator = PolicyEvaluator()
