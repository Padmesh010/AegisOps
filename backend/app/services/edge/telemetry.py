import uuid
import logging
from typing import Dict, Any, List
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.edge import DbIoTDevice

logger = logging.getLogger("app.services.edge.telemetry")

class IoTTelemetryService:
    async def ingest_device_reading(self, node_id: uuid.UUID, sensor_type: str, value: float) -> DbIoTDevice:
        """Process IoT telemetry metrics and update device status."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(DbIoTDevice).where(
                    DbIoTDevice.node_id == node_id,
                    DbIoTDevice.sensor_type == sensor_type
                )
            )
            device = res.scalar_one_or_none()
            
            if device:
                device.last_reading_val = value
            else:
                device = DbIoTDevice(
                    node_id=node_id,
                    sensor_type=sensor_type,
                    last_reading_val=value,
                    status="active"
                )
                
            session.add(device)
            await session.commit()
            return device

# Global telemetry service instance
iot_telemetry_service = IoTTelemetryService()
