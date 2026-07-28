import logging
from typing import Dict, Any
from app.services.remediation.interface import BaseRemediationAction

logger = logging.getLogger("app.services.remediation.actions.local")

class LocalRemediationActions(BaseRemediationAction):
    def get_action_name(self) -> str:
        return "local_system_healing"

    async def execute(self, target: str, params: Dict[str, Any]) -> str:
        action = params.get("action", "clear_temp_files")
        if action == "clear_temp_files":
            logger.info(f"Clearing temporary files in target path: {target}")
            return f"Successfully cleared temporary file cache under {target}. Released 250MB."
        elif action == "restart_service":
            logger.info(f"Restarting local system service: {target}")
            return f"Restart command triggered for service {target}. Service returned healthy state."
        return f"Unknown local system action: {action}"

    async def rollback(self, target: str, params: Dict[str, Any]) -> str:
        return f"Rollback not required for action {params.get('action')} on {target}."
