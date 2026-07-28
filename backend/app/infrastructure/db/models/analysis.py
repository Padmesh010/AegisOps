import uuid
from sqlalchemy import String, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class InvestigationHistory(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "investigation_history"

    incident_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("incidents.id"), nullable=False)
    ai_provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model_used: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(20), nullable=False, default="v1.0")
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    analysis_result: Mapped[dict] = mapped_column(JSON, nullable=False)
    token_usage_prompt: Mapped[int] = mapped_column(nullable=False, default=0)
    token_usage_completion: Mapped[int] = mapped_column(nullable=False, default=0)
    execution_time_ms: Mapped[int] = mapped_column(nullable=False, default=0)

    incident: Mapped["Incident"] = relationship("Incident", back_populates="investigations")
    recommendations: Mapped[list["Recommendation"]] = relationship(
        "Recommendation", back_populates="investigation", cascade="all, delete-orphan"
    )

class Recommendation(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "remediation_recommendations"

    investigation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigation_history.id"), nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_resource: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False, default=1)

    investigation: Mapped["InvestigationHistory"] = relationship("InvestigationHistory", back_populates="recommendations")

from app.infrastructure.db.models.incident import Incident
