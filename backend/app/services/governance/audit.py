import json
import hashlib
import logging
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.governance import DbAuditEvent

logger = logging.getLogger("app.services.governance.audit")

class ImmutableAuditLogService:
    def calculate_event_hash(self, event_type: str, actor_id: str, action: str, target_id: str, payload: dict) -> str:
        """Compute SHA256 integrity hash of event parameters payload to enable tamper-evidence checks."""
        h_payload = json.dumps(payload, sort_keys=True)
        raw_str = f"{event_type}|{actor_id}|{action}|{target_id}|{h_payload}"
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

    async def log_audit_event(
        self,
        event_type: str,
        actor_id: str,
        action: str,
        target_id: str,
        payload: dict
    ) -> DbAuditEvent:
        """Sign and persist an audit event trace to the database logs."""
        chk = self.calculate_event_hash(event_type, actor_id, action, target_id, payload)
        
        async with TestingSessionLocal() as session:
            event = DbAuditEvent(
                event_type=event_type,
                actor_id=actor_id,
                action=action,
                target_id=target_id,
                payload_json=payload,
                checksum_sha256=chk
            )
            session.add(event)
            await session.commit()
            return event

# Global audit service instance
audit_logger = ImmutableAuditLogService()
