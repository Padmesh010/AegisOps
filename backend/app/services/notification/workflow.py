import logging
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.notification import DbWorkflowDefinition

logger = logging.getLogger("app.services.notification.workflow")

class WorkflowExecutionEngine:
    async def process_event_workflows(self, trigger_type: str, event_payload: dict) -> None:
        """Query active workflow configurations matching trigger types and run actions sequentially."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(DbWorkflowDefinition).where(
                    DbWorkflowDefinition.trigger_type == trigger_type,
                    DbWorkflowDefinition.is_active == True
                )
            )
            workflows = res.scalars().all()
            
            for workflow in workflows:
                logger.info(f"Executing automation workflow: {workflow.name}")
                steps = workflow.steps_definition.get("steps", [])
                
                for step in steps:
                    action = step.get("action")
                    target = step.get("target")
                    
                    if action == "send_notification":
                        from app.services.notification.engine import notification_engine
                        msg = f"Workflow trigger {trigger_type} for event: {str(event_payload)}"
                        await notification_engine.dispatch_notification(target, msg)
                    elif action == "trigger_ai_analysis":
                        incident_id = event_payload.get("incident_id")
                        if incident_id:
                            from app.services.analysis.service import ai_investigator
                            import uuid
                            asyncio.create_task(ai_investigator.run_investigation(uuid.UUID(incident_id)))
                            
# Global workflow execution engine instance
workflow_engine = WorkflowExecutionEngine()

import asyncio
