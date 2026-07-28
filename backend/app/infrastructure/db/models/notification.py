import uuid
from sqlalchemy import String, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class NotificationChannel(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "notification_channels"

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    channel_type: Mapped[str] = mapped_column(String(20), nullable=False)  # email, slack, teams
    config_json: Mapped[dict] = mapped_column(JSON, nullable=False)

class DbNotificationHistory(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "notification_history"

    channel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("notification_channels.id"), nullable=False)
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")  # pending, sent, failed
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(nullable=False, default=0)

class DbEscalationPolicy(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "escalation_policies"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    escalate_after_minutes: Mapped[int] = mapped_column(nullable=False, default=15)
    target_role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)

class DbOnCallSchedule(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "oncall_schedules"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    rotation_period_days: Mapped[int] = mapped_column(nullable=False, default=7)
    active_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

class DbWorkflowDefinition(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "workflow_definitions"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    trigger_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., 'on_incident'
    steps_definition: Mapped[dict] = mapped_column(JSON, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
