from typing import List, Dict, Any

class ComplianceEngine:
    def map_to_frameworks(self, findings: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Aggregate security findings, mapping them to standard CIS and OWASP Top 10 indicators."""
        report = {
            "CIS-Benchmarks": [],
            "OWASP-Top-10": []
        }
        
        for f in findings:
            cve = f.get("cve_id", "")
            if "SECRET" in cve:
                report["OWASP-Top-10"].append({
                    "control": "A02:2021-Cryptographic Failures",
                    "finding": f
                })
                report["CIS-Benchmarks"].append({
                    "control": "Section 4.2 - Secrets Management",
                    "finding": f
                })
            elif "VULN" in cve:
                report["OWASP-Top-10"].append({
                    "control": "A06:2021-Vulnerable and Outdated Components",
                    "finding": f
                })
                
        return report

# Global compliance engine instance
compliance_engine = ComplianceEngine()
