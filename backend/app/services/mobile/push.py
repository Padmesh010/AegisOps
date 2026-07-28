import logging
from typing import Dict, Any

logger = logging.getLogger("app.services.mobile.push")

class PushNotificationService:
    async def send_web_push(self, push_token: str, title: str, body: str) -> bool:
        """Mock dispatching browser push notification to target device endpoint."""
        logger.info(f"Dispatching Push Notification card to token: {push_token}")
        logger.info(f"Payload - Title: {title} | Body: {body}")
        # Always successful mock
        return True

# Global push service instance
push_service = PushNotificationService()
