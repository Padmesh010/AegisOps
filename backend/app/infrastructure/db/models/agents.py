import uuid
from sqlalchemy import String, ForeignKey, Text, Float, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbAgentSession(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_sessions"

    goal: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="running")  # running, success, failed, paused
    max_steps: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    current_step: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    messages: Mapped[list["DbAgentMessage"]] = relationship(
        "DbAgentMessage", back_populates="session", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["DbAgentTask"]] = relationship(
        "DbAgentTask", back_populates="session", cascade="all, delete-orphan"
    )

class DbAgentMessage(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_messages"

    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agent_sessions.id", ondelete="CASCADE"), nullable=False)
    sender: Mapped[str] = mapped_column(String(50), nullable=False)  # SREAgent, DevOpsAgent, user
    recipient: Mapped[str] = mapped_column(String(50), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    session: Mapped[DbAgentSession] = relationship(DbAgentSession, back_populates="messages")

class DbAgentTask(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_tasks"

    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agent_sessions.id", ondelete="CASCADE"), nullable=False)
    assigned_agent: Mapped[str] = mapped_column(String(50), nullable=False)
    task_description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)  # pending, running, completed, failed
    dependencies_json: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)

    session: Mapped[DbAgentSession] = relationship(DbAgentSession, back_populates="tasks")

class DbAgentToolExecution(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_tool_executions"

    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agent_sessions.id", ondelete="CASCADE"), nullable=False)
    agent_name: Mapped[str] = mapped_column(String(50), nullable=False)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    input_args_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    output_result_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    execution_duration_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="success", nullable=False)

class DbAgentApproval(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_approvals"

    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agent_sessions.id", ondelete="CASCADE"), nullable=False)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)  # infrastructure_scaling, restart_vm
    target_resource: Mapped[str] = mapped_column(String(255), nullable=False)
    parameters_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)  # pending, approved, rejected, timeout
    decision_reason: Mapped[str] = mapped_column(Text, nullable=True)
