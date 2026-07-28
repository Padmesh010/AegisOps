import uuid
from datetime import datetime
from sqlalchemy import DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.utils.time import get_utc_now
from app.utils.uuid import generate_uuid

class BaseModel(DeclarativeBase):
    """Base declarative class for all database entities."""
    pass

class UUIDMixin:
    """Mixin adding cryptographically secure UUIDv4 as primary key."""
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid
    )

class TimestampMixin:
    """Mixin tracking record creation and modification times in UTC."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now,
        onupdate=get_utc_now,
        nullable=False
    )

class SoftDeleteMixin:
    """Mixin supporting soft-delete semantics for auditable tables."""
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def delete(self) -> None:
        self.is_deleted = True
        self.deleted_at = get_utc_now()
