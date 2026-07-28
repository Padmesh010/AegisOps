import uuid
from sqlalchemy import String, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbArtifactTemplate(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "artifact_templates"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., 'dockerfile', 'terraform'
    template_content: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0.0")

class DbGeneratedArtifact(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "generated_artifacts"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    template_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("artifact_templates.id"), nullable=True)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    code_content: Mapped[str] = mapped_column(Text, nullable=False)
    validation_status: Mapped[str] = mapped_column(String(20), nullable=False, default="unverified")
    validation_errors: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User")

class DbGenerationHistory(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "generation_history"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    prompt_used: Mapped[str] = mapped_column(Text, nullable=False)
    ai_provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model_used: Mapped[str] = mapped_column(String(50), nullable=False)
    token_usage_total: Mapped[int] = mapped_column(nullable=False, default=0)

    user: Mapped["User"] = relationship("User")

from app.infrastructure.db.models.user import User
