import logging
from typing import List, Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.agents import DbAgentSession, DbAgentTask

logger = logging.getLogger("app.services.agents.planner")

class GoalPlanner:
    async def create_execution_plan(self, session_id: uuid.UUID, goal: str) -> List[DbAgentTask]:
        """Decompose user goal into subtasks, assign them to specialized agents, and save them in the DB."""
        tasks = []
        
        # Deconstruct heuristic based on keywords
        goal_lower = goal.lower()
        
        async with TestingSessionLocal() as session:
            if "cost" in goal_lower or "rightsize" in goal_lower:
                # Assign to DevOps agent
                t1 = DbAgentTask(
                    session_id=session_id,
                    assigned_agent="DevOpsAgent",
                    task_description="Scan cloud resources cost inventories and identify rightsizing savings options.",
                    status="pending"
                )
                tasks.append(t1)
            elif "incident" in goal_lower or "cpu" in goal_lower:
                # Assign to SRE and Kubernetes agents
                t1 = DbAgentTask(
                    session_id=session_id,
                    assigned_agent="SREAgent",
                    task_description="Run investigation diagnostics over metrics timeline and find root causes.",
                    status="pending"
                )
                t2 = DbAgentTask(
                    session_id=session_id,
                    assigned_agent="KubernetesAgent",
                    task_description="Re-scale Pod replicas or execute node restarts to heal the system.",
                    status="pending"
                )
                tasks.extend([t1, t2])
            else:
                # Fallback generic task list
                t1 = DbAgentTask(
                    session_id=session_id,
                    assigned_agent="SREAgent",
                    task_description="Analyze general operations goals and review health indicators.",
                    status="pending"
                )
                tasks.append(t1)
                
            for t in tasks:
                session.add(t)
            await session.commit()
            
            # Fetch loaded instances with UUID keys
            return tasks

# Global planner instance
goal_planner = GoalPlanner()

import uuid
