import logging
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.notification import NotificationChannel, DbNotificationHistory
from app.services.notification.adapters.slack import slack_adapter

logger = logging.getLogger("app.services.notification.engine")

class NotificationDeliveryEngine:
    async def dispatch_notification(self, channel_name: str, message: str) -> bool:
        """Load target channel configuration settings and execute specific adapter deliveries."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(NotificationChannel).where(NotificationChannel.name == channel_name)
            )
            channel = res.scalar_one_or_none()
            if not channel:
                logger.error(f"Cannot dispatch notification: channel '{channel_name}' not configured in database.")
                return False

            status = "failed"
            error = None
            
            # Resolve delivery channel type
            if channel.channel_type == "slack":
                webhook_url = channel.config_json.get("webhook_url", "")
                success = await slack_adapter.send_slack_notification(webhook_url, message)
                status = "sent" if success else "failed"
                if not success:
                    error = "Failed to dispatch POST requests to target webhook"
            else:
                # Mock email SMTP delivery
                logger.info(f"Mock email dispatched: {message}")
                status = "sent"
                
            # Log history
            history = DbNotificationHistory(
                channel_id=channel.id,
                recipient=channel.config_json.get("recipient", "system"),
                body=message,
                status=status,
                error_message=error
            )
            session.add(history)
            await session.commit()
            
            return status == "sent"

# Global delivery engine instance
notification_engine = NotificationDeliveryEngine()
