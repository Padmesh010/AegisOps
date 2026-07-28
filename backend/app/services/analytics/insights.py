import logging
from typing import Dict, Any
from app.providers.ai.manager import ai_manager
from app.providers.ai.models import ModelRequest, ChatMessage

logger = logging.getLogger("app.services.analytics.insights")

class AIInsightsGenerator:
    async def generate_weekly_report(self, kpi_data: Dict[str, Any], incidents_count: int) -> str:
        """Compose prompts with SLA logs and MTTR values, requesting AI summaries reports."""
        prompt = (
            f"Write a professional weekly SRE executive operations summary report based on these metrics:\n"
            f"- Weekly Incidents Triggered: {incidents_count}\n"
            f"- Platform KPIs: {str(kpi_data)}\n"
            "Format the report in markdown with sections for: Executive Summary, Key Risks, and Operational Improvements."
        )
        
        req = ModelRequest(
            model="gpt-3.5-turbo",
            messages=[ChatMessage(role="user", content=prompt)]
        )
        
        try:
            response = await ai_manager.generate_completion_with_fallback(req)
            return response.content
        except Exception as err:
            logger.error(f"Failed to generate weekly AI operations summary report: {str(err)}")
            return "# Weekly SRE Operations Report\n*Report generation offline.*"

# Global generator instance
insights_generator = AIInsightsGenerator()
