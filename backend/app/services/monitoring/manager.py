import asyncio
from typing import Dict, Set
from fastapi import WebSocket

class TelemetrySubscriptionManager:
    def __init__(self) -> None:
        # Maps target_id string to active WebSocket clients subscribing to it
        self._subscriptions: Dict[str, Set[WebSocket]] = {}

    def subscribe(self, target_id: str, ws: WebSocket) -> None:
        """Register a client WebSocket connection to metrics updates of target."""
        if target_id not in self._subscriptions:
            self._subscriptions[target_id] = set()
        self._subscriptions[target_id].add(ws)

    def unsubscribe(self, target_id: str, ws: WebSocket) -> None:
        """Deregister client connection from metrics updates."""
        if target_id in self._subscriptions:
            self._subscriptions[target_id].discard(ws)
            if not self._subscriptions[target_id]:
                del self._subscriptions[target_id]

    async def broadcast_metric_update(self, target_id: str, payload: dict) -> None:
        """Publish a metric snapshot update to all active listener connections."""
        if target_id not in self._subscriptions:
            return
        
        dead_connections = set()
        for ws in self._subscriptions[target_id]:
            try:
                await ws.send_json(payload)
            except Exception:
                dead_connections.add(ws)
                
        # Clean up failed socket streams
        for ws in dead_connections:
            self.unsubscribe(target_id, ws)

# Global broker singleton
telemetry_broker = TelemetrySubscriptionManager()
