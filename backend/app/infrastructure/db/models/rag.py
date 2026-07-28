import uuid
from sqlalchemy import String, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models.base import BaseModel, UUIDMixin, TimestampMixin

class DbKnowledgeDocument(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "rag_documents"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    doc_type: Mapped[str] = mapped_column(String(50), nullable=False)  # markdown, runbook, config
    version: Mapped[int] = mapped_column(default=1, nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    chunks: Mapped[list["DbKnowledgeChunk"]] = relationship(
        "DbKnowledgeChunk", back_populates="document", cascade="all, delete-orphan"
    )

class DbKnowledgeChunk(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "rag_chunks"

    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("rag_documents.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding_json: Mapped[dict] = mapped_column(JSON, nullable=False)  # Mock float values mappings
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    document: Mapped[DbKnowledgeDocument] = relationship(DbKnowledgeDocument, back_populates="chunks")

class DbMemoryRecord(BaseModel, UUIDMixin, TimestampMixin):
    __tablename__ = "rag_memories"

    session_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="session")  # user, team, agent
    memory_key: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    memory_value: Mapped[str] = mapped_column(Text, nullable=False)
