import csv
import io
from typing import List, Dict

class DataExporter:
    def export_kpis_to_csv(self, kpis: List[Dict[str, Any]]) -> str:
        """Serialize a list of KPI dictionaries into standard CSV lines text."""
        output = io.StringIO()
        if not kpis:
            return ""
            
        writer = csv.DictWriter(output, fieldnames=kpis[0].keys())
        writer.writeheader()
        writer.writerows(kpis)
        return output.getvalue()

# Global exporter instance
data_exporter = DataExporter()

from typing import Any
