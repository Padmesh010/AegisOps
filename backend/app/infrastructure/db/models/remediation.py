import uuid
from sqlalchemy import String, ForeignKey, Text, Float, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class RemediationPolicy(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "remediation_policies"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_metric: Mapped[str] = mapped_column(String(100), nullable=False)
    action_plugin: Mapped[str] = mapped_column(String(50), nullable=False)
    risk_allowance: Mapped[str] = mapped_column(String(20), nullable=False, default="low")
    approval_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class RemediationPlan(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "remediation_plans"

    incident_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("incidents.id"), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending_approval")
    steps_data: Mapped[dict] = mapped_column(JSON, nullable=False)

    steps: Mapped[list["RemediationStep"]] = relationship(
        "RemediationStep", back_populates="plan", cascade="all, delete-orphan"
    )
    approvals: Mapped[list["RemediationApproval"]] = relationship(
        "RemediationApproval", back_populates="plan", cascade="all, delete-orphan"
    )

class RemediationStep(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "remediation_steps"

    plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("remediation_plans.id"), nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    execution_logs: Mapped[str] = mapped_column(Text, nullable=True)

    plan: Mapped["RemediationPlan"] = relationship("RemediationPlan", back_populates="steps")

class RemediationApproval(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "remediation_approvals"

    plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("remediation_plans.id"), nullable=False)
    approver_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    decision: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    comments: Mapped[str] = mapped_column(Text, nullable=True)

    plan: Mapped["RemediationPlan"] = relationship("RemediationPlan", back_populates="approvals")
    approver: Mapped["User"] = relationship("User")

from app.infrastructure.db.models.user import User
