from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseCollector(ABC):
    @abstractmethod
    def get_collector_name(self) -> str:
        """Return the unique string key of the collector strategy."""
        pass

    @abstractmethod
    async def collect_metrics(self) -> Dict[str, float]:
        """Scrape metrics values mapping label indicators to float quantities."""
        pass
