from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAgent(ABC):
    @abstractmethod
    def get_role_name(self) -> str:
        """Return the unique role name of the agent (e.g. SREAgent)."""
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of string capabilities."""
        pass

    @abstractmethod
    async def process_task(self, task_description: str, context: Dict[str, Any]) -> str:
        """Process a given sub-task, returning the text execution result."""
        pass
