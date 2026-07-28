import pytest
import uuid
from app.services.analysis.context import context_builder
from app.services.analysis.prompt import prompt_engine
from app.services.analysis.parser import response_parser

@pytest.mark.anyio
async def test_ai_prompt_generation() -> None:
    context = {
        "incident": {"title": "CPU Overload", "severity": "critical", "description": "CPU is at 100%"},
        "telemetry": [{"time": "2026-07-26", "target": "host1", "value": 100.0}],
        "timeline": []
    }
    prompt = prompt_engine.generate_prompt(context)
    assert "CPU Overload" in prompt
    assert "telemetry" in prompt.lower()

@pytest.mark.anyio
async def test_ai_response_parsing() -> None:
    raw = (
        "```json\n"
        "{\n"
        '  "summary": "Nginx instance is down",\n'
        '  "root_cause": "OOM killer terminated process",\n'
        '  "confidence_score": 90.0,\n'
        '  "remediation_steps": ["Restart Nginx", "Increase VM RAM"],\n'
        '  "risk_score": 20.0\n'
        "}\n"
        "```"
    )
    result = response_parser.parse_ai_response(raw)
    assert result["confidence_score"] == 90.0
    assert "Restart Nginx" in result["remediation_steps"]
