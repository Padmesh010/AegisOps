from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin
from app.core.enums import AIProviderType

class DbAIProvider(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "ai_providers"

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    provider_type: Mapped[AIProviderType] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    models: Mapped[list["DbAIModel"]] = relationship(
        "DbAIModel", back_populates="provider", cascade="all, delete-orphan"
    )

class DbAIModel(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "ai_models"

    provider_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_providers.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    context_length: Mapped[int] = mapped_column(default=4096, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    provider: Mapped[DbAIProvider] = relationship(DbAIProvider, back_populates="models")
    benchmarks: Mapped[list["DbAIBenchmark"]] = relationship(
        "DbAIBenchmark", back_populates="model", cascade="all, delete-orphan"
    )

class DbAIBenchmark(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "ai_benchmarks"

    model_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_models.id", ondelete="CASCADE"), nullable=False)
    latency_ms: Mapped[int] = mapped_column(nullable=False)
    tokens_per_sec: Mapped[Optional[float]] = mapped_column(nullable=True)
    success_rate: Mapped[float] = mapped_column(default=1.0, nullable=False)

    model: Mapped[DbAIModel] = relationship(DbAIModel, back_populates="benchmarks")
import uuid
