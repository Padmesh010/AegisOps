import pytest
from app.services.monitoring.local import LocalCollector

@pytest.mark.anyio
async def test_local_metrics_collector() -> None:
    collector = LocalCollector()
    metrics = await collector.collect_metrics()
    
    assert "cpu_utilization_percent" in metrics
    assert "memory_utilization_percent" in metrics
    assert "disk_utilization_percent" in metrics
    assert isinstance(metrics["cpu_utilization_percent"], float)
