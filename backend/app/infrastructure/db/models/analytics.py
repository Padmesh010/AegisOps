import uuid
from sqlalchemy import String, ForeignKey, Float, DateTime, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbSLADefinition(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "sla_definitions"

    service_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    target_availability: Mapped[float] = mapped_column(Float, nullable=False, default=99.9)  # percent
    description: Mapped[str] = mapped_column(Text, nullable=True)

class DbSLOObjective(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "slo_objectives"

    sla_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sla_definitions.id"), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    operator: Mapped[str] = mapped_column(String(10), nullable=False, default="less_than")

class DbKPIValue(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "kpi_values"

    kpi_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
