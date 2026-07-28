import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin
from app.utils.time import get_utc_now

class DbDeviceRegistration(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "mobile_device_registrations"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    push_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    device_type: Mapped[str] = mapped_column(String(50), nullable=False, default="android")  # android, ios, web
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

class DbOfflineSyncLog(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "mobile_sync_logs"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    last_synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, nullable=False)
    synced_entities_count: Mapped[int] = mapped_column(default=0, nullable=False)
