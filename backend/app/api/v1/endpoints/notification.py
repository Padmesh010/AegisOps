from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.notification import NotificationChannel
from app.services.notification.engine import notification_engine

router = APIRouter()

@router.post("/dispatch", response_model=dict)
async def dispatch_system_notification(
    channel_name: str,
    message: str,
    user: Any = Depends(get_current_user)
) -> dict:
    success = await notification_engine.dispatch_notification(channel_name, message)
    return {"status": "sent" if success else "failed"}

@router.post("/channels", status_code=201)
async def configure_notification_channel(
    name: str,
    channel_type: str,
    webhook_url: str,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    channel = NotificationChannel(
        name=name,
        channel_type=channel_type,
        config_json={"webhook_url": webhook_url}
    )
    db.add(channel)
    await db.commit()
    return {"status": "configured", "channel": name}

from typing import Any
