import logging
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.edge import DbEdgeNode
from app.utils.time import get_utc_now

logger = logging.getLogger("app.services.edge.fleet_manager")

class EdgeFleetManager:
    async def register_edge_node(self, name: str, site_id: str, arch: str = "x86_64") -> DbEdgeNode:
        """Register a new edge site computing node."""
        async with TestingSessionLocal() as session:
            node = DbEdgeNode(
                name=name,
                site_id=site_id,
                hardware_arch=arch,
                status="online"
            )
            session.add(node)
            await session.commit()
            return node

    async def checkin_node_heartbeat(self, node_id: uuid.UUID) -> bool:
        """Process heartbeat check-in for edge node, updating last_seen timestamp."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(select(DbEdgeNode).where(DbEdgeNode.id == node_id))
            node = res.scalar_one_or_none()
            if not node:
                return False
                
            node.last_heartbeat_at = get_utc_now()
            node.status = "online"
            session.add(node)
            await session.commit()
            return True

# Global fleet manager instance
edge_fleet_manager = EdgeFleetManager()

import uuid
