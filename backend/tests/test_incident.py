import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.incident.manager import incident_manager
from app.infrastructure.db.models.incident import Incident

@pytest.mark.anyio
async def test_incident_triggering_and_deduplication(db_session: AsyncSession) -> None:
    # Trigger first incident
    inc1 = await incident_manager.trigger_incident(
        title="High Memory Usage Alert",
        severity="critical",
        description="Memory usage reached 95% on local_host"
    )
    assert inc1.id is not None
    assert inc1.status == "triggered"
    
    # Trigger same incident (should deduplicate and return same object)
    inc2 = await incident_manager.trigger_incident(
        title="High Memory Usage Alert",
        severity="critical",
        description="Memory usage reached 96% on local_host"
    )
    assert inc1.id == inc2.id
