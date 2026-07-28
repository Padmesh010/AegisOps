from fastapi import APIRouter, Depends, HTTPException
from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.repositories.incident import IncidentRepository
from app.services.incident.manager import incident_manager

router = APIRouter()

@router.get("", response_model=List[dict])
async def list_active_incidents(
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> List[dict]:
    repo = IncidentRepository(db)
    incidents = await repo.get_active_incidents()
    return [
        {
            "id": str(i.id),
            "title": i.title,
            "status": i.status,
            "severity": i.severity,
            "description": i.description,
            "created_at": i.created_at.isoformat() if i.created_at else None
        } for i in incidents
    ]

@router.post("/{incident_id}/resolve", status_code=204)
async def resolve_incident(
    incident_id: str,
    user: Any = Depends(get_current_user)
) -> None:
    await incident_manager.update_incident_status(
        incident_id=incident_id,
        status="resolved",
        message="Incident resolved manually by user."
    )

from typing import Any
