import pytest
from app.services.finops.rightsizing import rightsizing_engine
from app.services.finops.carbon import carbon_engine

def test_rightsizing_options():
    resources = [
        {"id": "i-1", "cpu_avg": 2.0, "size": "t3.large"},
        {"id": "i-2", "cpu_avg": 12.0, "size": "t3.large"},
        {"id": "i-3", "cpu_avg": 50.0, "size": "t3.large"}
    ]
    recs = rightsizing_engine.identify_rightsizing_options(resources)
    assert len(recs) == 2
    assert recs[0]["resource_id"] == "i-1"
    assert "Downsize t3.large to t3.small" in recs[0]["action"]
    assert recs[1]["resource_id"] == "i-2"
    assert "Downsize t3.large to t3.medium" in recs[1]["action"]

def test_carbon_footprint_estimates():
    # US East grid multiplier is 0.45. Large instance is 250W.
    # 250W * 10h = 2500Wh = 2.5kWh. 2.5 * 0.45 = 1.125kg
    kg = carbon_engine.estimate_co2_kg("large", 10.0, "us-east-1")
    assert kg == 1.125
