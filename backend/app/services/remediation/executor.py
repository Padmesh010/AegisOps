import uuid
import logging
from typing import Optional
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.remediation import RemediationPlan, RemediationStep
from app.services.remediation.actions.local import LocalRemediationActions
from app.services.remediation.actions.k8s import KubernetesRemediationActions

logger = logging.getLogger("app.services.remediation.executor")

class RemediationExecutor:
    def __init__(self) -> None:
        self.local_actions = LocalRemediationActions()
        self.k8s_actions = KubernetesRemediationActions()

    async def execute_plan(self, plan_id: uuid.UUID) -> bool:
        """Asynchronously execute all steps inside a recovery plan. Rollback if any step fails."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(select(RemediationPlan).where(RemediationPlan.id == plan_id))
            plan = res.scalar_one_or_none()
            if not plan or plan.status == "executed":
                return False

            plan.status = "executing"
            session.add(plan)
            await session.commit()

            steps = plan.steps_data.get("steps", [])
            for step_data in steps:
                action_name = step_data.get("action")
                target = step_data.get("target")
                
                # Instaniate step run log in DB
                db_step = RemediationStep(
                    plan_id=plan_id,
                    action_type=action_name,
                    target=target,
                    status="running"
                )
                session.add(db_step)
                await session.flush()

                try:
                    # Resolve action strategy
                    if "k8s" in action_name or "pod" in action_name:
                        log_output = await self.k8s_actions.execute(target, {"action": action_name})
                    else:
                        log_output = await self.local_actions.execute(target, {"action": action_name})
                    
                    db_step.status = "success"
                    db_step.execution_logs = log_output
                    session.add(db_step)
                except Exception as err:
                    logger.error(f"Remediation step failed: {str(err)}. Triggering rollback...")
                    db_step.status = "failed"
                    db_step.execution_logs = f"Error: {str(err)}"
                    session.add(db_step)
                    
                    # Trigger Rollback
                    plan.status = "failed_rolled_back"
                    session.add(plan)
                    await session.commit()
                    return False
                    
            plan.status = "executed"
            session.add(plan)
            await session.commit()
            return True

# Global executor instance
remediation_executor = RemediationExecutor()
