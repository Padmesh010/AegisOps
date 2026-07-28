import uuid
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbPlugin(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "plugins"

    plugin_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    trusted_publisher: Mapped[bool] = mapped_column(Boolean, default=False)

    versions: Mapped[list["DbPluginVersion"]] = relationship(
        "DbPluginVersion", back_populates="plugin", cascade="all, delete-orphan"
    )

class DbPluginVersion(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "plugin_versions"

    plugin_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("plugins.id"), nullable=False)
    version_string: Mapped[str] = mapped_column(String(20), nullable=False)
    entry_point_config: Mapped[str] = mapped_column(String(255), nullable=False)  # Module path inside dynamic loader
    checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False)

    plugin: Mapped["DbPlugin"] = relationship("DbPlugin", back_populates="versions")
