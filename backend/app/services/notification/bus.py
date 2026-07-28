import asyncio
import logging
from typing import Dict, List, Callable, Any

logger = logging.getLogger("app.services.notification.bus")

class EventBus:
    def __init__(self) -> None:
        # Maps event_type string key to list of subscriber callbacks
        self._subscribers: Dict[str, List[Callable[[dict], Any]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[dict], Any]) -> None:
        """Register a handler callback function to listen to specific event notifications."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    async def publish_event(self, event_type: str, payload: dict) -> None:
        """Asynchronously dispatch event parameters payload to all registered callbacks."""
        if event_type not in self._subscribers:
            return
            
        tasks = []
        for callback in self._subscribers[event_type]:
            if asyncio.iscoroutinefunction(callback):
                tasks.append(callback(payload))
            else:
                # Wrap sync call in executor
                loop = asyncio.get_running_loop()
                tasks.append(loop.run_in_executor(None, callback, payload))
                
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

# Global event bus instance
system_event_bus = EventBus()
