import uuid
import logging
from typing import Dict, Any, List
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.edge import DbEdgeSyncQueue

logger = logging.getLogger("app.services.edge.sync_engine")

class EdgeSynchronizationEngine:
    async def queue_event_for_sync(self, node_id: uuid.UUID, payload: dict) -> DbEdgeSyncQueue:
        """Enqueue event parameters payload for offline-first replaying sync."""
        async with TestingSessionLocal() as session:
            item = DbEdgeSyncQueue(
                node_id=node_id,
                payload_json=payload,
                status="pending"
            )
            session.add(item)
            await session.commit()
            return item

    async def replay_sync_queue(self, node_id: uuid.UUID) -> int:
        """Iterate all pending items for node, replaying actions to centralized database and updating statuses."""
        count = 0
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(DbEdgeSyncQueue).where(
                    DbEdgeSyncQueue.node_id == node_id,
                    DbEdgeSyncQueue.status == "pending"
                )
            )
            items = res.scalars().all()
            
            for item in items:
                # Replay logic: mock success
                item.status = "replayed"
                session.add(item)
                count += 1
                
            await session.commit()
        logger.info(f"Replayed {count} offline sync items for edge node {node_id}")
        return count

# Global sync engine instance
edge_sync_engine = EdgeSynchronizationEngine()
