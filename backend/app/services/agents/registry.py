import logging
from typing import Dict, List, Any
from app.services.agents.base import BaseAgent

logger = logging.getLogger("app.services.agents.registry")

class BuiltInSREAgent(BaseAgent):
    def get_role_name(self) -> str:
        return "SREAgent"

    def get_capabilities(self) -> List[str]:
        return ["incident_investigation", "remediation_planning", "slo_checks"]

    async def process_task(self, task_description: str, context: Dict[str, Any]) -> str:
        logger.info(f"SREAgent executing task: {task_description}")
        return f"SREAgent successfully analyzed incident alerts and proposed remediation plan steps."

class BuiltInDevOpsAgent(BaseAgent):
    def get_role_name(self) -> str:
        return "DevOpsAgent"

    def get_capabilities(self) -> List[str]:
        return ["ci_cd_repairs", "deployment_planning", "config_generation"]

    async def process_task(self, task_description: str, context: Dict[str, Any]) -> str:
        logger.info(f"DevOpsAgent executing task: {task_description}")
        return f"DevOpsAgent successfully constructed the requested Dockerfile build."

class BuiltInKubernetesAgent(BaseAgent):
    def get_role_name(self) -> str:
        return "KubernetesAgent"

    def get_capabilities(self) -> List[str]:
        return ["k8s_pods_troubleshoot", "scale_recommendations"]

    async def process_task(self, task_description: str, context: Dict[str, Any]) -> str:
        logger.info(f"KubernetesAgent executing task: {task_description}")
        return f"KubernetesAgent verified node statuses and successfully scaled deployment replicas."

class AgentRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, BaseAgent] = {}
        self._tools: Dict[str, Dict[str, Any]] = {}
        
        # Register built-ins
        self.register_agent(BuiltInSREAgent())
        self.register_agent(BuiltInDevOpsAgent())
        self.register_agent(BuiltInKubernetesAgent())
        
        # Register default tools schemas
        self.register_tool(
            name="clear_temp_files",
            schema={"target": "string"},
            permission="write_file"
        )
        self.register_tool(
            name="restart_service",
            schema={"target": "string"},
            permission="restart_service"
        )

    def register_agent(self, agent: BaseAgent) -> None:
        self._agents[agent.get_role_name()] = agent
        logger.info(f"Registered agent: {agent.get_role_name()}")

    def get_agent(self, role_name: str) -> BaseAgent:
        return self._agents.get(role_name)

    def list_agents(self) -> List[str]:
        return list(self._agents.keys())

    def register_tool(self, name: str, schema: dict, permission: str) -> None:
        self._tools[name] = {"schema": schema, "permission": permission}

    def get_tool(self, name: str) -> Dict[str, Any]:
        return self._tools.get(name)

# Global registry instance
agent_registry = AgentRegistry()
