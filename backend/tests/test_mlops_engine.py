import pytest
from app.services.mlops.prompt import prompt_template_manager
from app.services.mlops.evaluator import model_evaluator

def test_prompt_formatting():
    template = "Deploying {{service}} with replica count {{count}}."
    res = prompt_template_manager.format_prompt(template, {"service": "web-app", "count": 3})
    assert res == "Deploying web-app with replica count 3."

def test_model_generations_evaluator():
    # 1. Non-hallucinatory compliant text
    res = model_evaluator.evaluate_generation(
        "restart container", "Container successfully restarted. System reports healthy."
    )
    assert res["hallucination_index"] == 0.0
    assert res["safety_compliant"] is True
    assert res["quality_rating"] == "passed"
    
    # 2. Hallucinatory response
    res_hal = model_evaluator.evaluate_generation(
        "get user", "I don't have access to this real-time data."
    )
    assert res_hal["hallucination_index"] > 50.0
    assert res_hal["quality_rating"] == "failed"
