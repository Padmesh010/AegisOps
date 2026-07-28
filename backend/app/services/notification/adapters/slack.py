import httpx
import logging
from typing import Dict, Any

logger = logging.getLogger("app.services.notification.adapters.slack")

class SlackAdapter:
    async def send_slack_notification(self, webhook_url: str, message: str) -> bool:
        """Post a formatted notification card to the target Slack channel webhook."""
        if not webhook_url:
            return False
            
        async with httpx.AsyncClient(timeout=5.0) as client:
            payload = {
                "text": "AegisOps Alert System Notification",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*AegisOps operational update:*\n{message}"
                        }
                    }
                ]
            }
            try:
                response = await client.post(webhook_url, json=payload)
                if response.status_code != 200:
                    logger.error(f"Slack webhook endpoint returned {response.status_code}: {response.text}")
                    return False
                return True
            except Exception as err:
                logger.error(f"Failed to post notification message to Slack: {str(err)}")
                return False

# Global adapter instance
slack_adapter = SlackAdapter()
