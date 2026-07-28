import logging
from typing import Dict, Any, List

logger = logging.getLogger("app.services.automation.scheduler")

class WorkflowSchedulerManager:
    def __init__(self) -> None:
        self._schedules: Dict[str, str] = {}  # workflow_id -> cron expression

    def add_schedule(self, workflow_id: str, cron_expression: str) -> None:
        """Register a workflow trigger schedule."""
        self._schedules[workflow_id] = cron_expression
        logger.info(f"Registered schedule for workflow {workflow_id}: {cron_expression}")

    def remove_schedule(self, workflow_id: str) -> None:
        """Deregister a workflow trigger schedule."""
        if workflow_id in self._schedules:
            del self._schedules[workflow_id]
            logger.info(f"Removed schedule for workflow {workflow_id}")

# Global scheduler instance
workflow_scheduler = WorkflowSchedulerManager()
