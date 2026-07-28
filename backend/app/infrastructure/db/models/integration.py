import uuid
from sqlalchemy import String, ForeignKey, Text, JSON, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbIntegrationAccount(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "integration_accounts"

    provider_type: Mapped[str] = mapped_column(String(50), nullable=False)  # aws, gcp, azure
    account_name: Mapped[str] = mapped_column(String(100), nullable=False)
    encrypted_credentials: Mapped[str] = mapped_column(Text, nullable=False)
    sync_status: Mapped[str] = mapped_column(String(20), nullable=False, default="idle")

    resources: Mapped[list["DbCloudResource"]] = relationship(
        "DbCloudResource", back_populates="account", cascade="all, delete-orphan"
    )

class DbCloudResource(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "cloud_resources"

    account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("integration_accounts.id"), nullable=False)
    resource_arn: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    resource_name: Mapped[str] = mapped_column(String(150), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)  # ec2, s3, EKS
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=True)

    account: Mapped["DbIntegrationAccount"] = relationship("DbIntegrationAccount", back_populates="resources")

class DbKubernetesCluster(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "kubernetes_clusters"

    cluster_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    api_server_endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    certificate_authority_data: Mapped[str] = mapped_column(Text, nullable=False)
    namespaces_list: Mapped[dict] = mapped_column(JSON, nullable=True)  # List of namespaces
    pod_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

class DbSyncLog(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "integration_sync_logs"

    account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("integration_accounts.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="success")
    message: Mapped[str] = mapped_column(Text, nullable=True)

class DbCostRecommendation(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "cost_recommendations"

    resource_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cloud_resources.id"), nullable=False)
    recommendation_type: Mapped[str] = mapped_column(String(50), nullable=False)
    current_cost_est: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    projected_cost_est: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    savings_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    action_steps: Mapped[str] = mapped_column(Text, nullable=False)
