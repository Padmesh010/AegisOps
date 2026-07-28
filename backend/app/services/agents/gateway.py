import logging
from app.services.dashboard.gateway import websocket_gateway

logger = logging.getLogger("app.services.agents.gateway")

class AgentGatewayNotifier:
    async def publish_agent_state(self, session_id: str, status: str, step: int) -> None:
        """Broadcast agent planning state steps updates to listening frontends."""
        logger.info(f"Broadcasting agent state session {session_id} -> {status}")
        await websocket_gateway.broadcast_event({
            "event": "agent_state_update",
            "session_id": session_id,
            "status": status,
            "step": step
        })

# Global notifier instance
agent_gateway = AgentGatewayNotifier()
