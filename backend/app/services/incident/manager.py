import logging
from datetime import datetime, timezone
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.incident import Incident, IncidentEvent

logger = logging.getLogger("app.services.incident.manager")

class IncidentManager:
    async def trigger_incident(self, title: str, severity: str, description: str) -> Incident:
        """Create and persist an active incident in the database, avoiding duplicates."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            # Check for existing triggered/active incidents with similar titles
            res = await session.execute(
                select(Incident).where(
                    Incident.title == title,
                    Incident.status != "resolved",
                    Incident.is_deleted == False  # type: ignore
                )
            )
            existing = res.scalar_one_or_none()
            if existing:
                # Log incident occurrence event log instead of duplicate
                event = IncidentEvent(
                    incident_id=existing.id,
                    event_type="occurrence",
                    message=f"Deduplicated alert occurrence: {description}"
                )
                session.add(event)
                await session.commit()
                return existing

            # Create new incident record
            incident = Incident(
                title=title,
                status="triggered",
                severity=severity,
                description=description
            )
            session.add(incident)
            await session.flush()
            
            # Record initial timeline log
            event = IncidentEvent(
                incident_id=incident.id,
                event_type="creation",
                message=f"Incident initialized by monitoring threshold rules: {description}"
            )
            session.add(event)
            await session.commit()
            
            # Fire event notification via system event bus
            from app.services.notification.bus import system_event_bus
            await system_event_bus.publish_event(
                "incident.triggered",
                {"incident_id": str(incident.id), "title": title, "severity": severity}
            )
            
            return incident

    async def update_incident_status(self, incident_id: str, status: str, message: str) -> None:
        """Transitions state (Triggered -> Active -> Resolved)."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            import uuid
            res = await session.execute(select(Incident).where(Incident.id == uuid.UUID(incident_id)))
            incident = res.scalar_one_or_none()
            if not incident:
                return

            incident.status = status
            if status == "resolved":
                incident.resolved_at = datetime.now(timezone.utc)
            
            event = IncidentEvent(
                incident_id=incident.id,
                event_type="status_change",
                message=message
            )
            session.add(event)
            session.add(incident)
            await session.commit()

# Global manager instance
incident_manager = IncidentManager()
