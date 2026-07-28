from typing import Dict, Type
from app.providers.ai.interface import AIProvider
from app.providers.ai.ollama import OllamaProvider
from app.providers.ai.openai import OpenAIProvider

class AIProviderFactory:
    def __init__(self) -> None:
        self._providers: Dict[str, Type[AIProvider]] = {}
        # Register standard built-in providers
        self.register_provider("ollama", OllamaProvider)
        self.register_provider("openai", OpenAIProvider)

    def register_provider(self, name: str, provider_cls: Type[AIProvider]) -> None:
        """Register a new provider class strategy matching the target name key."""
        self._providers[name.lower()] = provider_cls

    def get_provider(self, name: str) -> AIProvider:
        """Resolve and instantiate a registered provider instance."""
        provider_name = name.lower()
        if provider_name not in self._providers:
            from app.core.exceptions import ValidationError
            raise ValidationError(f"AI Provider '{name}' is not registered or supported by the hub.")
        
        provider_cls = self._providers[provider_name]
        return provider_cls()

# Global factory singleton
ai_factory = AIProviderFactory()
