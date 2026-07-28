import json
import logging
from typing import Dict, Any
from pydantic import BaseModel, Field

logger = logging.getLogger("app.services.analysis.parser")

class StructuredAnalysis(BaseModel):
    summary: str = Field(..., description="Executive summary of the issue")
    root_cause: str = Field(..., description="Estimated root cause description")
    confidence_score: float = Field(..., ge=0.0, le=100.0)
    remediation_steps: list[str] = Field(default_factory=list)
    risk_score: float = Field(default=0.0, ge=0.0, le=100.0)

class ResponseParser:
    def parse_ai_response(self, raw_content: str) -> Dict[str, Any]:
        """Verify, validate, and clean raw text into target structured JSON parameters."""
        try:
            # 1. Strip potential Markdown wraps
            cleaned = raw_content.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            parsed = json.loads(cleaned)
            # Run schema checks using Pydantic
            validated = StructuredAnalysis(**parsed)
            return validated.model_dump()
        except Exception as err:
            logger.warn(f"Failed to parse LLM response into structured format: {str(err)}. Content: {raw_content}")
            # Fallback to simple structure
            return {
                "summary": "Diagnostics failed to parse into structured format.",
                "root_cause": "Unknown operational error.",
                "confidence_score": 10.0,
                "remediation_steps": ["Inspect system alerts manually."],
                "risk_score": 50.0
            }

# Global parser instance
response_parser = ResponseParser()
