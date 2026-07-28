import pytest
from app.services.automation.designer import workflow_designer
from app.services.automation.ai_assistant import ai_workflow_assistant

def test_workflow_dag_validations():
    dag_json = {
        "nodes": [
            {"id": "node-1", "type": "HTTP", "config": {"url": "https://example.com"}},
            {"id": "node-2", "type": "Python", "config": {}}
        ]
    }
    assert workflow_designer.validate_workflow_dag(dag_json) is True
    
    # Duplicate IDs -> invalid
    dag_invalid = {
        "nodes": [
            {"id": "node-1", "type": "HTTP"},
            {"id": "node-1", "type": "Python"}
        ]
    }
    assert workflow_designer.validate_workflow_dag(dag_invalid) is False

@pytest.mark.asyncio
async def test_ai_workflow_generation():
    # Verify fallback triggers safely without crash
    dag_str = await ai_workflow_assistant.generate_workflow_dag("build workflow for cpu alert")
    assert dag_str is not None
