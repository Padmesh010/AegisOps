import uuid
from sqlalchemy import String, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbWorkflowDefinition(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "auto_workflow_definitions"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    trigger_type: Mapped[str] = mapped_column(String(50), nullable=False)  # alert, manual, schedule
    dag_nodes_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    version: Mapped[int] = mapped_column(default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)  # draft, published

    executions: Mapped[list["DbWorkflowExecution"]] = relationship(
        "DbWorkflowExecution", back_populates="definition", cascade="all, delete-orphan"
    )

class DbWorkflowExecution(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "auto_workflow_executions"

    definition_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auto_workflow_definitions.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="running", nullable=False)  # running, success, failed, paused
    trigger_payload_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    execution_logs: Mapped[str] = mapped_column(Text, nullable=True)

    definition: Mapped[DbWorkflowDefinition] = relationship(DbWorkflowDefinition, back_populates="executions")
    tasks: Mapped[list["DbWorkflowTask"]] = relationship(
        "DbWorkflowTask", back_populates="execution", cascade="all, delete-orphan"
    )

class DbWorkflowTask(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "auto_workflow_tasks"

    execution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auto_workflow_executions.id", ondelete="CASCADE"), nullable=False)
    node_id: Mapped[str] = mapped_column(String(100), nullable=False)
    node_type: Mapped[str] = mapped_column(String(50), nullable=False)  # HTTP, AIPrompt, Approval
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    retry_count: Mapped[int] = mapped_column(default=0, nullable=False)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)

    execution: Mapped[DbWorkflowExecution] = relationship(DbWorkflowExecution, back_populates="tasks")
