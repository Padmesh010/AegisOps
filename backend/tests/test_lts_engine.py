import pytest
from app.services.lts.hardening import lts_hardening_engine
from app.services.lts.diagnostics import diagnostic_bundle_service

def test_security_csp_headers():
    headers = lts_hardening_engine.get_security_headers()
    assert "Content-Security-Policy" in headers
    assert headers["X-Frame-Options"] == "DENY"

def test_diagnostics_log_bundle():
    zip_bytes = diagnostic_bundle_service.create_log_bundle()
    assert len(zip_bytes) > 0
    assert zip_bytes[:4] == b"PK\x03\x04"  # standard ZIP header magic bytes signature
