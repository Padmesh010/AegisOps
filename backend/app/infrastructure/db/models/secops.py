import uuid
from sqlalchemy import String, ForeignKey, Text, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbSecurityScan(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "security_scans"

    scan_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., 'secrets', 'container', 'iac'
    target_path: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    execution_duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ai_summary: Mapped[str] = mapped_column(Text, nullable=True)

    findings: Mapped[list["DbScanFinding"]] = relationship(
        "DbScanFinding", back_populates="scan", cascade="all, delete-orphan"
    )

class DbScanFinding(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "security_findings"

    scan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("security_scans.id"), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")  # e.g., low, medium, high, critical
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    line_number: Mapped[int] = mapped_column(Integer, nullable=True)
    cve_id: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    remediation: Mapped[str] = mapped_column(Text, nullable=True)

    scan: Mapped["DbSecurityScan"] = relationship("DbSecurityScan", back_populates="findings")

class DbSBOMRecord(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "sbom_records"

    project_name: Mapped[str] = mapped_column(String(100), nullable=False)
    sbom_format: Mapped[str] = mapped_column(String(20), nullable=False, default="cyclonedx")
    sbom_content: Mapped[dict] = mapped_column(JSON, nullable=False)
