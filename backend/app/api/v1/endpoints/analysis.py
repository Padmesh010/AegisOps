from fastapi import APIRouter, Depends, HTTPException
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.services.analysis.service import ai_investigator
from app.infrastructure.db.repositories.analysis import InvestigationRepository

router = APIRouter()

@router.post("/investigate/{incident_id}", response_model=dict)
async def trigger_ai_investigation(
    incident_id: str,
    user: Any = Depends(get_current_user)
) -> dict:
    try:
        parsed_id = uuid.UUID(incident_id)
        history = await ai_investigator.run_investigation(parsed_id)
        return {
            "investigation_id": str(history.id),
            "confidence_score": history.confidence_score,
            "analysis": history.analysis_result
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"AI Investigation failed: {str(err)}")

@router.get("/{incident_id}", response_model=dict)
async def get_investigation_results(
    incident_id: str,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    repo = InvestigationRepository(db)
    parsed_id = uuid.UUID(incident_id)
    history_list = await repo.get_by_incident_id(parsed_id)
    if not history_list:
        raise HTTPException(status_code=404, detail="No investigations history found for incident.")
        
    latest = history_list[-1]
    return {
        "id": str(latest.id),
        "ai_provider": latest.ai_provider,
        "model_used": latest.model_used,
        "confidence_score": latest.confidence_score,
        "analysis": latest.analysis_result,
        "created_at": latest.created_at.isoformat() if latest.created_at else None
    }

from typing import Any
