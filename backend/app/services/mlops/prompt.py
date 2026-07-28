import logging
from typing import Dict, Any, List
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.mlops import DbPromptVersion

logger = logging.getLogger("app.services.mlops.prompt")

class PromptTemplateManager:
    async def create_prompt_version(
        self,
        prompt_key: str,
        version: str,
        template_str: str,
        params: dict
    ) -> DbPromptVersion:
        """Register a new versioned prompt template."""
        async with TestingSessionLocal() as session:
            version_item = DbPromptVersion(
                prompt_key=prompt_key,
                version=version,
                template_str=template_str,
                parameters_json=params
            )
            session.add(version_item)
            await session.commit()
            return version_item

    def format_prompt(self, template: str, variables: Dict[str, Any]) -> str:
        """Inject runtime variable bindings into prompt templates."""
        formatted = template
        for key, val in variables.items():
            formatted = formatted.replace(f"{{{{{key}}}}}", str(val))
            formatted = formatted.replace(f"{{{{ {key} }}}}", str(val))
        return formatted

# Global prompt template manager
prompt_template_manager = PromptTemplateManager()
