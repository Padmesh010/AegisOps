from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class GlobalSetting(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "global_settings"

    key: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    value: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
