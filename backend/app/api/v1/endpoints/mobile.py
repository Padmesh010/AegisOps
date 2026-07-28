from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.mobile import DbDeviceRegistration
from app.services.mobile.sync import offline_sync_service

router = APIRouter()

@router.post("/devices/register", response_model=dict)
async def register_mobile_device(
    push_token: str,
    device_type: str = "android",
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    device = DbDeviceRegistration(
        user_id=user.id,
        push_token=push_token,
        device_type=device_type
    )
    db.add(device)
    await db.commit()
    return {"status": "registered", "device_id": str(device.id)}

@router.get("/sync/delta", response_model=dict)
async def get_sync_delta(
    user: Any = Depends(get_current_user)
) -> dict:
    delta = await offline_sync_service.get_offline_sync_delta(user.id)
    return delta

from typing import Any
