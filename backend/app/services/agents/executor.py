import uuid
import logging
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.agents import DbAgentSession, DbAgentTask, DbAgentMessage
from app.services.agents.registry import agent_registry
from app.services.agents.safety import safety_limits

logger = logging.getLogger("app.services.agents.executor")

class TaskExecutionEngine:
    async def execute_session_tasks(self, session_id: uuid.UUID) -> bool:
        """Sequential loop executor that fetches pending tasks, runs them through the registry, and checks safety guards."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(DbAgentSession).where(DbAgentSession.id == session_id)
            )
            agent_session = res.scalar_one_or_none()
            if not agent_session or agent_session.status != "running":
                return False

            # Fetch tasks
            res_tasks = await session.execute(
                select(DbAgentTask).where(
                    DbAgentTask.session_id == session_id,
                    DbAgentTask.status == "pending"
                )
            )
            tasks = res_tasks.scalars().all()
            
            for task in tasks:
                # 1. Check safety limiters depth
                if not safety_limits.can_proceed(agent_session.current_step, agent_session.max_steps):
                    agent_session.status = "failed"
                    task.status = "failed"
                    session.add(agent_session)
                    session.add(task)
                    await session.commit()
                    logger.warn(f"Agent session {session_id} execution depth limit exceeded. Halting.")
                    return False
                
                # Update status
                task.status = "running"
                agent_session.current_step += 1
                session.add(task)
                session.add(agent_session)
                await session.flush()

                # 2. Get target agent
                agent = agent_registry.get_agent(task.assigned_agent)
                if not agent:
                    task.status = "failed"
                    session.add(task)
                    await session.commit()
                    continue
                    
                # 3. Process execution
                try:
                    result_text = await agent.process_task(task.task_description, {})
                    task.status = "completed"
                    
                    # Log structured message
                    msg = DbAgentMessage(
                        session_id=session_id,
                        sender=task.assigned_agent,
                        recipient="user",
                        body=result_text
                    )
                    session.add(msg)
                    session.add(task)
                except Exception as err:
                    logger.error(f"Agent execution failure: {str(err)}")
                    task.status = "failed"
                    session.add(task)
                    
            agent_session.status = "success"
            session.add(agent_session)
            await session.commit()
            return True

# Global executor instance
task_executor = TaskExecutionEngine()
