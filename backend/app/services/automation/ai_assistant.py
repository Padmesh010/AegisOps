import logging
from app.providers.ai.manager import ai_manager
from app.providers.ai.models import ModelRequest, ChatMessage

logger = logging.getLogger("app.services.automation.ai_assistant")

class AIWorkflowAssistant:
    async def generate_workflow_dag(self, prompt: str) -> str:
        """Query LLM via Provider Hub to compile natural language request into workflow JSON schema."""
        system_prompt = (
            "You are an expert operations automation engineer.\n"
            "Synthesize a JSON representation of an AegisOps DAG workflow containing 'nodes' and 'edges'.\n"
            "Return ONLY raw JSON, without markdown formatting wrappers like ``` or annotations."
        )
        
        req = ModelRequest(
            model="gpt-3.5-turbo",
            messages=[
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=prompt)
            ]
        )
        
        try:
            response = await ai_manager.generate_completion_with_fallback(req)
            return response.content
        except Exception as err:
            logger.error(f"Failed to generate workflow DAG using AI: {str(err)}")
            return '{"nodes": [], "edges": []}'

# Global assistant instance
ai_workflow_assistant = AIWorkflowAssistant()
