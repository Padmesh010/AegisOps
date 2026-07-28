from typing import Dict, Any

class TemplateEngine:
    def render_template(self, template_str: str, variables: Dict[str, Any]) -> str:
        """Inject template tags with variable parameter mappings."""
        rendered = template_str
        for key, val in variables.items():
            tag = f"{{{{ {key} }}}}"
            rendered = rendered.replace(tag, str(val))
            # Support tag variations without spaces
            tag_nospace = f"{{{{{key}}}}}"
            rendered = rendered.replace(tag_nospace, str(val))
        return rendered

# Global template engine instance
template_engine = TemplateEngine()
