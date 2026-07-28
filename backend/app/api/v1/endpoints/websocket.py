from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
from app.services.dashboard.gateway import websocket_gateway
from app.services.monitoring.manager import telemetry_broker

router = APIRouter()
logger = logging.getLogger("app.api.v1.endpoints.websocket")

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str) -> None:
    """Accept real-time subscriber socket streams, mapping subscriptions and heartbeats."""
    await websocket_gateway.connect_client(client_id, websocket)
    try:
        while True:
            # Wait for message mapping subscription commands
            data = await websocket.receive_json()
            command = data.get("command", "")
            target_id = data.get("target_id", "")
            
            if command == "subscribe":
                telemetry_broker.subscribe(target_id, websocket)
                await websocket.send_json({"status": "subscribed", "target": target_id})
            elif command == "unsubscribe":
                telemetry_broker.unsubscribe(target_id, websocket)
                await websocket.send_json({"status": "unsubscribed", "target": target_id})
            elif command == "ping":
                await websocket.send_json({"status": "pong"})
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: {client_id}")
    except Exception as err:
        logger.error(f"Error on WebSocket session client {client_id}: {str(err)}")
    finally:
        websocket_gateway.disconnect_client(client_id)
