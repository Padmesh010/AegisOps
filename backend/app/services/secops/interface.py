from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScannerAdapter(ABC):
    @abstractmethod
    def get_scanner_name(self) -> str:
        """Return the unique string key identifier of the scanner."""
        pass

    @abstractmethod
    async def run_scan(self, target_path: str) -> List[Dict[str, Any]]:
        """Run scanning checks. Return list of normalized findings dictionaries."""
        pass
