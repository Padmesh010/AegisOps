import uuid
from sqlalchemy import String, ForeignKey, Text, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbPromptVersion(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "mlops_prompt_versions"

    prompt_key: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    version: Mapped[str] = mapped_column(String(20), nullable=False)
    template_str: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    parameters_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    runs: Mapped[list["DbMLRun"]] = relationship(
        "DbMLRun", back_populates="prompt_version", cascade="all, delete-orphan"
    )

class DbMLRun(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "mlops_runs"

    experiment_name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    prompt_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mlops_prompt_versions.id", ondelete="CASCADE"), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    parameters_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    metrics_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)  # score, latency_ms
    status: Mapped[str] = mapped_column(String(20), default="success", nullable=False)

    prompt_version: Mapped[DbPromptVersion] = relationship(DbPromptVersion, back_populates="runs")

class DbModelDeployment(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "mlops_deployments"

    model_name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    deployment_stage: Mapped[str] = mapped_column(String(50), nullable=False)  # production, staging, shadow, canary
    target_traffic_pct: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
