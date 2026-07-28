import uuid
from sqlalchemy import String, ForeignKey, Text, Float, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbCostRecord(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "finops_cost_records"

    provider: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # aws, gcp, azure
    resource_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    service_type: Mapped[str] = mapped_column(String(100), index=True, nullable=False)  # compute, storage, db
    cost_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    tags_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

class DbBudget(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "finops_budgets"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    limit_amount: Mapped[float] = mapped_column(Float, nullable=False)
    current_spending: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    alert_threshold_pct: Mapped[float] = mapped_column(Float, default=80.0, nullable=False)
    team_id: Mapped[str] = mapped_column(String(100), index=True, nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

class DbCarbonLog(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "finops_carbon_logs"

    resource_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    co2_emissions_kg_est: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
