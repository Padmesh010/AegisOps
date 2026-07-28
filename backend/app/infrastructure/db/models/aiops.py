import uuid
from typing import Optional
from sqlalchemy import String, Boolean, JSON, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbAIOpsModel(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "aiops_models"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    version: Mapped[str] = mapped_column(String(20), nullable=False)
    model_type: Mapped[str] = mapped_column(String(50), nullable=False)  # isolation_forest, dbscan, regression
    parameters_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    metrics_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class DbAnomalyLog(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "aiops_anomaly_logs"

    target_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    metric_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    strategy_used: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="warning")
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)

class DbCapacityForecast(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "aiops_capacity_forecasts"

    resource_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # cpu, memory, disk
    target_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    forecast_window_hours: Mapped[int] = mapped_column(nullable=False, default=24)
    growth_rate_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    estimated_exhaustion_hours: Mapped[float] = mapped_column(Float, nullable=False, default=-1.0)
    confidence_lower: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    confidence_upper: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

class DbOperationalHealthScore(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "aiops_health_scores"

    scope_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # organization, team, service, cluster
    scope_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    health_score: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    breakdown_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

class DbAlertCluster(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "aiops_alert_clusters"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    incident_ids_list: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    reduction_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

class DbFailurePrediction(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "aiops_failure_predictions"

    target_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    failure_type: Mapped[str] = mapped_column(String(100), default="node_exhaustion", nullable=False)
    probability: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
