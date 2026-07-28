from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.services.generation.engine import devops_generator

router = APIRouter()

@router.post("/generate", response_model=dict)
async def generate_devops_config(
    target_type: str,
    prompt: str,
    user: Any = Depends(get_current_user)
) -> dict:
    try:
        artifact = await devops_generator.generate_devops_artifact(
            user_id=user.id,
            target_type=target_type,
            prompt=prompt
        )
        return {
            "artifact_id": str(artifact.id),
            "target_type": artifact.target_type,
            "code": artifact.code_content,
            "status": artifact.validation_status,
            "errors": artifact.validation_errors
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

from typing import Any
