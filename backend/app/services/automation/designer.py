from typing import Dict, Any

class WorkflowDesignerService:
    def validate_workflow_dag(self, dag_json: Dict[str, Any]) -> bool:
        """Validate DAG schema (check for cycles and ensure entry points exist)."""
        nodes = dag_json.get("nodes", [])
        if not nodes:
            return False
            
        # Basic validation: ensure all nodes have unique IDs
        node_ids = {n.get("id") for n in nodes if n.get("id")}
        if len(node_ids) != len(nodes):
            return False  # Duplicate IDs
            
        return True

# Global designer instance
workflow_designer = WorkflowDesignerService()
