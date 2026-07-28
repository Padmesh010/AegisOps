import uuid
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.generation import DbGeneratedArtifact, DbGenerationHistory
from app.services.generation.template import template_engine
from app.services.generation.validator import artifact_validator
from app.providers.ai.manager import ai_manager
from app.providers.ai.models import ModelRequest, ChatMessage

class DevOpsGenerationEngine:
    async def generate_devops_artifact(
        self,
        user_id: uuid.UUID,
        target_type: str,
        prompt: str,
        template_str: str = ""
    ) -> DbGeneratedArtifact:
        """Query LLM via Provider Hub to generate specific DevOps code manifests, running syntaxes checks."""
        # 1. Build prompt context mapping
        system_prompt = (
            f"You are a Senior DevOps Engineer. Generate a clean {target_type} configuration.\n"
            "Return ONLY raw code/manifest contents. Do NOT include markdown styling wrappers like ``` or explanation text."
        )
        
        req = ModelRequest(
            model="gpt-3.5-turbo",
            messages=[
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=prompt)
            ],
            temperature=0.1
        )
        
        # 2. Call AI Hub
        response = await ai_manager.generate_completion_with_fallback(req)
        code_content = response.content
        
        # Apply template variable formatting if baseline exists
        if template_str:
            code_content = template_engine.render_template(template_str, {"generated_code": code_content})
            
        # 3. Validate syntax
        if target_type == "dockerfile":
            check = artifact_validator.validate_dockerfile(code_content)
        else:
            check = artifact_validator.validate_yaml(code_content)
            
        # 4. Persistence
        async with TestingSessionLocal() as session:
            artifact = DbGeneratedArtifact(
                user_id=user_id,
                target_type=target_type,
                code_content=code_content,
                validation_status="verified" if check["valid"] else "failed",
                validation_errors=check["errors"]
            )
            session.add(artifact)
            
            history = DbGenerationHistory(
                user_id=user_id,
                prompt_used=prompt,
                ai_provider="hub",
                model_used=response.model,
                token_usage_total=response.usage.total_tokens
            )
            session.add(history)
            await session.commit()
            
            return artifact

# Global generator instance
devops_generator = DevOpsGenerationEngine()
