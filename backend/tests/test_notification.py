import pytest
from app.services.notification.bus import system_event_bus

@pytest.mark.anyio
async def test_event_bus_pub_sub() -> None:
    events_logged = []
    
    async def sample_subscriber(payload: dict) -> None:
        events_logged.append(payload)
        
    system_event_bus.subscribe("test.event", sample_subscriber)
    await system_event_bus.publish_event("test.event", {"val": "ping"})
    
    assert len(events_logged) == 1
    assert events_logged[0]["val"] == "ping"
