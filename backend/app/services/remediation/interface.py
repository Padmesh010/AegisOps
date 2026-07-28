from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseRemediationAction(ABC):
    @abstractmethod
    def get_action_name(self) -> str:
        """Unique key name of the action plugin."""
        pass

    @abstractmethod
    async def execute(self, target: str, params: Dict[str, Any]) -> str:
        """Run the remediation logic. Return execution string log details."""
        pass

    @abstractmethod
    async def rollback(self, target: str, params: Dict[str, Any]) -> str:
        """Rollback state prior to execution. Return logs."""
        pass
