import uuid
from sqlalchemy import String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbMetric(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "metrics_definition"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    snapshots: Mapped[list["DbMetricSnapshot"]] = relationship(
        "DbMetricSnapshot", back_populates="metric", cascade="all, delete-orphan"
    )

class DbMetricSnapshot(BaseModel, UUIDMixin):
    __tablename__ = "metrics_snapshots"

    metric_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("metrics_definition.id"), nullable=False)
    target_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    metric: Mapped["DbMetric"] = relationship("DbMetric", back_populates="snapshots")

class DbAlertThreshold(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "alert_thresholds"

    metric_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    warning_limit: Mapped[float] = mapped_column(Float, nullable=False)
    critical_limit: Mapped[float] = mapped_column(Float, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(nullable=False, default=60)
