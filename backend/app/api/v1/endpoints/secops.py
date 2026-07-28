from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.services.secops.engine import secops_scanner
from app.infrastructure.db.repositories.secops import SecurityScanRepository

router = APIRouter()

@router.post("/scan", response_model=dict)
async def trigger_security_scan(
    target_path: str,
    user: Any = Depends(get_current_user)
) -> dict:
    try:
        scan = await secops_scanner.execute_project_scan(target_path)
        return {
            "scan_id": str(scan.id),
            "status": scan.status,
            "duration_ms": scan.execution_duration_ms,
            "ai_summary": scan.ai_summary
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/scans", response_model=list[dict])
async def list_security_scans(
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> list[dict]:
    repo = SecurityScanRepository(db)
    scans = await repo.get_multi(limit=20)
    return [
        {
            "id": str(s.id),
            "scan_type": s.scan_type,
            "target": s.target_path,
            "status": s.status,
            "created_at": s.created_at.isoformat() if s.created_at else None
        } for s in scans
    ]

from typing import Any
