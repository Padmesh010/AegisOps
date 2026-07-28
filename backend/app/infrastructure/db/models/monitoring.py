import uuid
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class Cluster(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "monitoring_clusters"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    api_endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    token_secret_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

class Node(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "monitoring_nodes"

    cluster_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("monitoring_clusters.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
