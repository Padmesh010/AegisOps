import pytest
from app.services.aiops.anomaly import anomaly_engine
from app.services.aiops.forecaster import forecast_engine
from app.services.aiops.health_scoring import health_scoring_engine

def test_anomaly_zscore():
    history = [10.0, 10.0, 10.0, 10.0, 100.0]
    res = anomaly_engine.detect_zscore(history, threshold=1.5)
    assert res["anomalous"] is True
    assert res["score"] > 1.5

def test_anomaly_zscore_insufficient():
    res = anomaly_engine.detect_zscore([10.0])
    assert res["anomalous"] is False

@pytest.mark.asyncio
async def test_health_scoring_calculations():
    factors = {"cpu_spikes": 2.0, "slo_violations": 1.0}
    health = await health_scoring_engine.calculate_scope_health("service", "db-prod", factors)
    # 100 - (2 * 5.0) - (1 * 20.0) = 70.0
    assert health.health_score == 70.0
    assert health.scope_id == "db-prod"
