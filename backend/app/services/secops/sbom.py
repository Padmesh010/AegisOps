import json
from typing import List, Dict, Any

class SBOMGenerator:
    def generate_cyclonedx_sbom(self, project_name: str, dependencies: List[Dict[str, str]]) -> Dict[str, Any]:
        """Format dependency mappings into a standard CycloneDX JSON structure."""
        return {
            "bomFormat": "CycloneDX",
            "specVersion": "1.5",
            "serialNumber": "urn:uuid:a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
            "version": 1,
            "metadata": {
                "component": {
                    "name": project_name,
                    "type": "application"
                }
            },
            "components": [
                {
                    "name": dep["name"],
                    "version": dep.get("version", "latest"),
                    "type": "library",
                    "purl": f"pkg:npm/{dep['name']}@{dep.get('version', 'latest')}"
                } for dep in dependencies
            ]
        }

# Global SBOM generator instance
sbom_generator = SBOMGenerator()
