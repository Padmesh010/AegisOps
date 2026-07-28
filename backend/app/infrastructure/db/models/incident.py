from datetime import datetime
import uuid
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.core.enums import IncidentStatus, Severity

class Incident(BaseModel, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "incidents"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="triggered", index=True, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="warning", index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    events: Mapped[list["IncidentEvent"]] = relationship(
        "IncidentEvent", back_populates="incident", cascade="all, delete-orphan"
    )
    investigations: Mapped[list["InvestigationHistory"]] = relationship(
        "InvestigationHistory", back_populates="incident", cascade="all, delete-orphan"
    )

class IncidentEvent(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "incident_events"

    incident_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("incidents.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[str] = mapped_column(Text, nullable=True)

    incident: Mapped["Incident"] = relationship("Incident", back_populates="events")

from app.infrastructure.db.models.analysis import InvestigationHistory
