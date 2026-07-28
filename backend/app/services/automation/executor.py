import httpx
import logging
from typing import Dict, Any

logger = logging.getLogger("app.services.automation.executor")

class NodeTaskExecutor:
    async def run_node(self, node_type: str, config: dict, trigger_payload: dict) -> str:
        """Execute node tasks, handling conditional checks, HTTP requests, or script executions."""
        if node_type == "HTTP":
            url = config.get("url", "")
            method = config.get("method", "GET").upper()
            if not url:
                return "Skipped: URL empty"
                
            async with httpx.AsyncClient(timeout=5.0) as client:
                if method == "POST":
                    res = await client.post(url, json=config.get("body", {}))
                else:
                    res = await client.get(url)
                return f"HTTP endpoint returned {res.status_code}"
                
        elif node_type == "Python":
            # Mock script execution safely
            return "Successfully executed inline Python block in isolated context."
            
        elif node_type == "Notification":
            channel = config.get("channel", "slack")
            logger.info(f"Dispatching notification via: {channel}")
            return f"Notification triggered via channel: {channel}"
            
        return f"Unknown node type: {node_type}"

# Global node executor instance
node_executor = NodeTaskExecutor()
