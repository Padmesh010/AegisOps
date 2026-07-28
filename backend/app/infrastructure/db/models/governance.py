import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, Text, JSON, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbPolicy(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "gov_policies"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    rules_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    enforcement_mode: Mapped[str] = mapped_column(String(20), default="audit", nullable=False)  # audit, warn, enforce
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class DbComplianceFinding(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "gov_compliance_findings"

    framework: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # CIS, SOC2, GDPR
    rule_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # passed, failed, warning
    target_resource_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")

class DbRiskItem(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "gov_risks"

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # security, reliability, financial
    impact_level: Mapped[str] = mapped_column(String(20), nullable=False)  # high, medium, low
    likelihood_level: Mapped[str] = mapped_column(String(20), nullable=False)
    mitigation_steps: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

class DbAuditEvent(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "gov_audit_events"

    event_type: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    actor_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    target_id: Mapped[str] = mapped_column(String(100), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False)

class DbWaiver(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "gov_waivers"

    policy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("gov_policies.id", ondelete="CASCADE"), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    approved_by: Mapped[str] = mapped_column(String(100), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
