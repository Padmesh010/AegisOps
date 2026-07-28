import uuid
import logging
from typing import Dict, Any, List
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.automation import DbWorkflowDefinition, DbWorkflowExecution, DbWorkflowTask
from app.services.automation.executor import node_executor

logger = logging.getLogger("app.services.automation.engine")

class WorkflowExecutionEngine:
    async def execute_workflow(self, definition_id: uuid.UUID, trigger_payload: dict) -> DbWorkflowExecution:
        """Instantiate a workflow execution trace, evaluate DAG nodes list sequentially, and log outcomes."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(DbWorkflowDefinition).where(DbWorkflowDefinition.id == definition_id)
            )
            wf = res.scalar_one_or_none()
            if not wf or wf.status != "published":
                raise ValueError("Workflow definition not found or is in draft state.")
                
            execution = DbWorkflowExecution(
                definition_id=definition_id,
                status="running",
                trigger_payload_json=trigger_payload,
                execution_logs=""
            )
            session.add(execution)
            await session.flush()
            
            nodes = wf.dag_nodes_json.get("nodes", [])
            log_lines = []
            
            for node in nodes:
                node_id = node.get("id")
                node_type = node.get("type", "HTTP")
                
                db_task = DbWorkflowTask(
                    execution_id=execution.id,
                    node_id=node_id,
                    node_type=node_type,
                    status="running"
                )
                session.add(db_task)
                await session.flush()
                
                try:
                    # Run node task
                    log_output = await node_executor.run_node(node_type, node.get("config", {}), trigger_payload)
                    db_task.status = "success"
                    log_lines.append(f"Node {node_id} [{node_type}]: Success - {log_output}")
                except Exception as err:
                    db_task.status = "failed"
                    db_task.error_message = str(err)
                    log_lines.append(f"Node {node_id} [{node_type}]: Failed - {str(err)}")
                    execution.status = "failed"
                    session.add(db_task)
                    break
                    
                session.add(db_task)
                
            if execution.status == "running":
                execution.status = "success"
                
            execution.execution_logs = "\n".join(log_lines)
            session.add(execution)
            await session.commit()
            return execution

# Global engine instance
workflow_execution_engine = WorkflowExecutionEngine()
