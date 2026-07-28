from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.services.edge.fleet_manager import edge_fleet_manager
from app.services.edge.sync_engine import edge_sync_engine
from app.services.edge.telemetry import iot_telemetry_service

router = APIRouter()

@router.post("/nodes/register", response_model=dict)
async def register_node(
    name: str,
    site_id: str,
    arch: str = "x86_64",
    user: Any = Depends(get_current_user)
) -> dict:
    node = await edge_fleet_manager.register_edge_node(name, site_id, arch)
    return {"status": "registered", "node_id": str(node.id)}

@router.post("/nodes/{node_id}/heartbeat", response_model=dict)
async def heartbeat_checkin(
    node_id: str,
    user: Any = Depends(get_current_user)
) -> dict:
    parsed_id = uuid.UUID(node_id)
    success = await edge_fleet_manager.checkin_node_heartbeat(parsed_id)
    if not success:
        raise HTTPException(status_code=404, detail="Node not registered.")
    
    # Replay sync queue
    replayed = await edge_sync_engine.replay_sync_queue(parsed_id)
    return {"status": "online", "replayed_count": replayed}

@router.post("/telemetry/ingest", response_model=dict)
async def ingest_iot_telemetry(
    node_id: str,
    sensor_type: str,
    value: float,
    user: Any = Depends(get_current_user)
) -> dict:
    parsed_id = uuid.UUID(node_id)
    reading = await iot_telemetry_service.ingest_device_reading(parsed_id, sensor_type, value)
    return {"status": "ingested", "sensor": reading.sensor_type, "value": reading.last_reading_val}

from typing import Any
