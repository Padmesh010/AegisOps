import re
import os
from typing import List, Dict, Any
from app.services.secops.interface import BaseScannerAdapter

class GitleaksAdapter(BaseScannerAdapter):
    def get_scanner_name(self) -> str:
        return "gitleaks_secrets"

    async def run_scan(self, target_path: str) -> List[Dict[str, Any]]:
        """Scan folder files matching strings against simple key patterns."""
        findings = []
        
        # Simple regex targets
        token_pattern = re.compile(r"(?i)(api[-_]?key|secret[-_]?key|jwt[-_]?token|password)\s*[:=]\s*['\"][a-z0-9_\-]{8,}['\"]")
        
        # For validation simplicity, we check local scripts or config directories
        if not os.path.exists(target_path):
            return []
            
        try:
            for root, _, files in os.walk(target_path):
                for file in files:
                    if file.endswith((".py", ".env", ".toml", ".yml", ".json")):
                        full_path = os.path.join(root, file)
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            for idx, line in enumerate(f, 1):
                                if token_pattern.search(line):
                                    findings.append({
                                        "severity": "critical",
                                        "file_path": os.path.relpath(full_path, target_path),
                                        "line_number": idx,
                                        "cve_id": "SEC-SECRET-LEAK",
                                        "description": "Hardcoded credential token leak detected in source text line.",
                                        "remediation": "Move credential key to env variables injection config."
                                    })
        except Exception:
            pass
            
        return findings
