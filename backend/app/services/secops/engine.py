import uuid
import time
from typing import Dict, Any, List
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.secops import DbSecurityScan, DbScanFinding
from app.services.secops.adapters.gitleaks import GitleaksAdapter
from app.providers.ai.manager import ai_manager
from app.providers.ai.models import ModelRequest, ChatMessage

class SecurityScanningEngine:
    def __init__(self) -> None:
        self.gitleaks = GitleaksAdapter()

    async def execute_project_scan(self, target_path: str) -> DbSecurityScan:
        """Run standard scanner plugins, aggregate findings, and write a summary to the database."""
        start_time = time.perf_counter()
        
        # 1. Run Secrets Scan
        findings = await self.gitleaks.run_scan(target_path)
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        
        # 2. Invoke AI summary diagnostics if findings exist
        summary = "No security vulnerabilities or credentials leaks detected."
        if findings:
            prompt = (
                f"Analyze these DevSecOps scanner findings and summarize the risks:\n"
                f"{str(findings)}\n"
                "Return a concise 2-sentence summary and immediate patch recommendations."
            )
            req = ModelRequest(
                model="gpt-3.5-turbo",
                messages=[ChatMessage(role="user", content=prompt)]
            )
            try:
                res = await ai_manager.generate_completion_with_fallback(req)
                summary = res.content
            except Exception:
                summary = "Vulnerabilities detected. AI summary diagnostics offline."

        # 3. Persistence
        async with TestingSessionLocal() as session:
            scan = DbSecurityScan(
                scan_type="secrets",
                target_path=target_path,
                status="success",
                execution_duration_ms=duration_ms,
                ai_summary=summary
            )
            session.add(scan)
            await session.flush()
            
            for f in findings:
                db_finding = DbScanFinding(
                    scan_id=scan.id,
                    severity=f["severity"],
                    file_path=f["file_path"],
                    line_number=f["line_number"],
                    cve_id=f["cve_id"],
                    description=f["description"],
                    remediation=f["remediation"]
                )
                session.add(db_finding)
                
            await session.commit()
            return scan

# Global scanning engine instance
secops_scanner = SecurityScanningEngine()
