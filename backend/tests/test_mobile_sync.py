import pytest
from app.services.mobile.push import push_service

@pytest.mark.asyncio
async def test_mobile_web_push():
    success = await push_service.send_web_push("mock_token", "Alert!", "CPU utilization critical.")
    assert success is True
