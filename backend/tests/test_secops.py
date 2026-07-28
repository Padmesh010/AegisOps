import pytest
import tempfile
import os
from app.services.secops.adapters.gitleaks import GitleaksAdapter
from app.services.secops.policy import secops_policy

@pytest.mark.anyio
async def test_secrets_leaks_regex_scanner() -> None:
    adapter = GitleaksAdapter()
    
    # Create temporary file containing api key
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "config.py")
        with open(file_path, "w") as f:
            f.write('API_KEY = "key-1234567890"')
            
        findings = await adapter.run_scan(tmpdir)
        assert len(findings) == 1
        assert findings[0]["severity"] == "critical"
        assert "SECRET-LEAK" in findings[0]["cve_id"]

def test_secops_block_policy_engine() -> None:
    findings = [{"severity": "critical", "description": "credential leak"}]
    allowed = secops_policy.evaluate_findings(findings, ["critical"])
    assert allowed is False
    
    allowed_pass = secops_policy.evaluate_findings(findings, ["low"])
    assert allowed_pass is True
