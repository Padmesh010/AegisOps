import uuid
import logging
from typing import Optional
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.rag import DbMemoryRecord

logger = logging.getLogger("app.services.rag.memory")

class LongTermMemoryEngine:
    async def get_memory(self, session_id: uuid.UUID, key: str) -> Optional[str]:
        """Query memory record value from database."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(DbMemoryRecord).where(
                    DbMemoryRecord.session_id == session_id,
                    DbMemoryRecord.memory_key == key
                )
            )
            rec = res.scalar_one_or_none()
            return rec.memory_value if rec else None

    async def save_memory(self, session_id: uuid.UUID, key: str, value: str, scope: str = "session") -> None:
        """Store key-value memory record in database."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(DbMemoryRecord).where(
                    DbMemoryRecord.session_id == session_id,
                    DbMemoryRecord.memory_key == key
                )
            )
            rec = res.scalar_one_or_none()
            if rec:
                rec.memory_value = value
            else:
                rec = DbMemoryRecord(
                    session_id=session_id,
                    scope=scope,
                    memory_key=key,
                    memory_value=value
                )
            session.add(rec)
            await session.commit()

# Global memory engine instance
long_term_memory = LongTermMemoryEngine()
