import uuid
from sqlalchemy import String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbDashboard(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "dashboards"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="personal")  # personal, team, org
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User")
    widgets: Mapped[list["DbWidget"]] = relationship(
        "DbWidget", back_populates="dashboard", cascade="all, delete-orphan"
    )

class DbWidget(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "dashboard_widgets"

    dashboard_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dashboards.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # CPU, Incident, Notification
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    grid_layout: Mapped[dict] = mapped_column(JSON, nullable=False)  # {x, y, w, h}

    dashboard: Mapped["DbDashboard"] = relationship("DbDashboard", back_populates="widgets")
    configurations: Mapped[list["DbWidgetConfiguration"]] = relationship(
        "DbWidgetConfiguration", back_populates="widget", cascade="all, delete-orphan"
    )

class DbWidgetConfiguration(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "widget_configurations"

    widget_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dashboard_widgets.id"), nullable=False)
    config_key: Mapped[str] = mapped_column(String(50), nullable=False)
    config_value: Mapped[str] = mapped_column(String(255), nullable=False)

    widget: Mapped["DbWidget"] = relationship("DbWidget", back_populates="configurations")

class DbUserPreference(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "user_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    theme: Mapped[str] = mapped_column(String(30), nullable=False, default="Enterprise Dark")
    timezone: Mapped[str] = mapped_column(String(50), nullable=False, default="UTC")
    default_dashboard_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dashboards.id"), nullable=True)

    user: Mapped["User"] = relationship("User")

from app.infrastructure.db.models.user import User
