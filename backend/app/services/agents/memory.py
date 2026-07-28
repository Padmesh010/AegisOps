import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("app.services.agents.memory")

class AgentMemoryManager:
    def __init__(self) -> None:
        # Simple session memory mapping (session_id -> dict of key/values)
        self._memories: Dict[str, Dict[str, Any]] = {}

    def get_value(self, session_id: str, key: str) -> Optional[Any]:
        """Fetch memory item value from key-value registry."""
        if session_id in self._memories:
            return self._memories[session_id].get(key)
        return None

    def set_value(self, session_id: str, key: str, value: Any) -> None:
        """Store memory key-value pair."""
        if session_id not in self._memories:
            self._memories[session_id] = {}
        self._memories[session_id][key] = value
        logger.info(f"Session {session_id} memory set: {key} -> {str(value)}")

# Global memory manager instance
agent_memory = AgentMemoryManager()
