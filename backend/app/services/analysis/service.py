import uuid
import time
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.analysis import InvestigationHistory, Recommendation
from app.services.analysis.context import context_builder
from app.services.analysis.prompt import prompt_engine
from app.services.analysis.parser import response_parser
from app.providers.ai.manager import ai_manager
from app.providers.ai.models import ModelRequest, ChatMessage

class AIInvestigationService:
    async def run_investigation(self, incident_id: uuid.UUID) -> InvestigationHistory:
        """Run incident diagnostics, querying AI Provider Hub and storing results in database."""
        # 1. Build Context
        context = await context_builder.build_investigation_context(incident_id)
        
        # 2. Build prompts
        system_prompt = prompt_engine.get_system_prompt()
        user_prompt = prompt_engine.generate_prompt(context)
        
        req = ModelRequest(
            model="gpt-3.5-turbo",  # default model
            messages=[
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=user_prompt)
            ],
            temperature=0.2
        )
        
        # 3. Request LLM completion via AI manager
        start_time = time.perf_counter()
        # In test mode/fallback, if OpenAI is not configured, it will run fallbacks cleanly
        response = await ai_manager.generate_completion_with_fallback(req)
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        
        # 4. Parse response
        analysis = response_parser.parse_ai_response(response.content)
        
        # 5. Write history record to database
        async with TestingSessionLocal() as session:
            history = InvestigationHistory(
                incident_id=incident_id,
                ai_provider="hub",
                model_used=response.model,
                prompt_version="v1.0",
                confidence_score=analysis.get("confidence_score", 50.0),
                analysis_result=analysis,
                token_usage_prompt=response.usage.prompt_tokens,
                token_usage_completion=response.usage.completion_tokens,
                execution_time_ms=duration_ms
            )
            session.add(history)
            await session.flush()
            
            # Map recommendations
            for idx, step in enumerate(analysis.get("remediation_steps", [])):
                rec = Recommendation(
                    investigation_id=history.id,
                    action_type="remediation",
                    target_resource=context.get("incident", {}).get("title", "system"),
                    description=step,
                    risk_level="low" if analysis.get("risk_score", 0) < 40 else "medium",
                    priority=idx + 1
                )
                session.add(rec)
            
            await session.commit()
            return history

# Global service instance
ai_investigator = AIInvestigationService()
