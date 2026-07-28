import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, Text, JSON, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin
from app.utils.time import get_utc_now

class DbEdgeNode(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "edge_nodes"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    site_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="online", nullable=False)  # online, offline
    hardware_arch: Mapped[str] = mapped_column(String(50), nullable=False, default="x86_64")
    last_heartbeat_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, nullable=False)

class DbEdgeSyncQueue(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "edge_sync_queues"

    node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("edge_nodes.id", ondelete="CASCADE"), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)  # pending, replayed, failed
    retry_count: Mapped[int] = mapped_column(default=0, nullable=False)

class DbIoTDevice(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "edge_iot_devices"

    node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("edge_nodes.id", ondelete="CASCADE"), nullable=False)
    sensor_type: Mapped[str] = mapped_column(String(100), nullable=False)  # temperature, network_rtt
    last_reading_val: Mapped[float] = mapped_column(default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
