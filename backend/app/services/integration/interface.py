from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseCloudAdapter(ABC):
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the unique string key identifier of the cloud provider (e.g., 'aws')."""
        pass

    @abstractmethod
    async def discover_resources(self, credentials_json: dict) -> List[Dict[str, Any]]:
        """Query cloud provider APIs and return a list of standard resource maps."""
        pass
