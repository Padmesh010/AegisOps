from typing import Dict, Any

class PromptEngine:
    def get_system_prompt(self) -> str:
        return (
            "You are an elite Site Reliability Engineer (SRE) AI assistant.\n"
            "Analyze the operational telemetry context payload and diagnose the incident.\n"
            "Your output must be a clean JSON object containing the fields:\n"
            "- summary: A concise executive summary.\n"
            "- root_cause: Probable root cause of the incident.\n"
            "- confidence_score: Float value between 0.0 and 100.0.\n"
            "- remediation_steps: List of recommended actions.\n"
            "- risk_score: Risk score between 0.0 and 100.0."
        )

    def generate_prompt(self, context: Dict[str, Any]) -> str:
        """Compose user prompt injecting metric values, timeline logs and descriptions."""
        incident = context.get("incident", {})
        telemetry = context.get("telemetry", [])
        timeline = context.get("timeline", [])
        
        telemetry_str = "\n".join([f"- {t['time']}: {t['target']} reported value {t['value']}" for t in telemetry])
        timeline_str = "\n".join([f"- [{t['type']}] {t['msg']}" for t in timeline])

        return (
            f"Incident Title: {incident.get('title')}\n"
            f"Severity: {incident.get('severity')}\n"
            f"Description: {incident.get('description')}\n\n"
            f"Telemetry Trend History:\n{telemetry_str}\n\n"
            f"Audit Log Timeline Events:\n{timeline_str}\n\n"
            f"Diagnose this incident and return the requested JSON object format."
        )

# Global engine instance
prompt_engine = PromptEngine()
