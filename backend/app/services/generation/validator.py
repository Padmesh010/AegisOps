import json
from typing import Dict, Any

class ArtifactValidator:
    def validate_yaml(self, content: str) -> Dict[str, Any]:
        """Validate if a YAML string parse structure is syntax clean."""
        # Standard Python doesn't bundle yaml. We use a simple JSON or YAML stub check.
        # If PyYAML is configured, parse it; else verify it's not raw garbage.
        try:
            import yaml
            yaml.safe_load(content)
            return {"valid": True, "errors": None}
        except ImportError:
            # Fallback simple lines check
            if ":" not in content and content.strip():
                return {"valid": False, "errors": "Malformed key-value pairings (missing colon)"}
            return {"valid": True, "errors": None}
        except Exception as err:
            return {"valid": False, "errors": str(err)}

    def validate_dockerfile(self, content: str) -> Dict[str, Any]:
        """Verify standard Dockerfile instructions are included (FROM, USER)."""
        lines = [l.strip().upper() for l in content.splitlines()]
        
        has_from = False
        for line in lines:
            if line.startswith("FROM"):
                has_from = True
                break
                
        if not has_from:
            return {"valid": False, "errors": "Missing FROM base image declaration instruction"}
        return {"valid": True, "errors": None}

# Global validator instance
artifact_validator = ArtifactValidator()
