import logging

logger = logging.getLogger("app.services.agents.safety")

class AgentSafetyLimiter:
    def can_proceed(self, current_step: int, max_steps: int) -> bool:
        """Verify the agent task execution step stays strictly below max planning depth boundaries."""
        if current_step >= max_steps:
            logger.warn(f"Execution boundary exceeded: step {current_step} >= max {max_steps}")
            return False
        return True

# Global safety instance
safety_limits = AgentSafetyLimiter()
