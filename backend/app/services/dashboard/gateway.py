import asyncio
import logging
from typing import Dict, Set
from fastapi import WebSocket, status

logger = logging.getLogger("app.services.dashboard.gateway")

class WebSocketGatewayManager:
    def __init__(self) -> None:
        # Maps user session string key to active connection WebSocket object
        self._active_connections: Dict[str, WebSocket] = {}

    async def connect_client(self, client_id: str, ws: WebSocket) -> None:
        """Accept WebSocket connection, register connection state."""
        await ws.accept()
        self._active_connections[client_id] = ws
        logger.info(f"WebSocket client connected: {client_id}")

    def disconnect_client(self, client_id: str) -> None:
        """Deregister client connection."""
        if client_id in self._active_connections:
            del self._active_connections[client_id]
            logger.info(f"WebSocket client disconnected: {client_id}")

    async def send_personal_message(self, client_id: str, message: dict) -> None:
        """Deliver metrics updates specifically to a single target client."""
        if client_id in self._active_connections:
            try:
                await self._active_connections[client_id].send_json(message)
            except Exception:
                self.disconnect_client(client_id)

    async def broadcast_event(self, message: dict) -> None:
        """Broadcast event payloads to all currently open socket connections."""
        dead_clients = []
        for client_id, ws in self._active_connections.items():
            try:
                await ws.send_json(message)
            except Exception:
                dead_clients.append(client_id)
                
        for client in dead_clients:
            self.disconnect_client(client)

# Global gateway instance
websocket_gateway = WebSocketGatewayManager()
