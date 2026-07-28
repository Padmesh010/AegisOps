import pytest
from app.services.generation.detector import project_detector
from app.services.generation.template import template_engine
from app.services.generation.validator import artifact_validator

def test_project_type_detection() -> None:
    res = project_detector.detect_project_type(["requirements.txt", "app.py"])
    assert res["language"] == "Python"
    assert "python" in res["docker_base"]

def test_template_variable_substitution() -> None:
    res = template_engine.render_template("Hello {{ name }}!", {"name": "SRE"})
    assert res == "Hello SRE!"

def test_artifact_syntax_validation() -> None:
    check = artifact_validator.validate_dockerfile("FROM node:20-alpine\nRUN npm install")
    assert check["valid"] is True
    
    check_fail = artifact_validator.validate_dockerfile("RUN npm install")
    assert check_fail["valid"] is False
