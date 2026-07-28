from typing import List, Dict, Any

class SecopsPolicyEngine:
    def evaluate_findings(self, findings: List[Dict[str, Any]], blocked_severities: List[str]) -> bool:
        """Validate if audit scan findings breach block limits (e.g. deny builds if critical is found)."""
        for finding in findings:
            severity = finding.get("severity", "low").lower()
            if severity in [s.lower() for s in blocked_severities]:
                return False  # Failed policy validation
        return True

# Global policy engine instance
secops_policy = SecopsPolicyEngine()
