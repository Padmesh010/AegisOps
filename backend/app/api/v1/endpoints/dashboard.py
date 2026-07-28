from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.dashboard import DbDashboard
from app.infrastructure.db.repositories.dashboard import DashboardRepository

router = APIRouter()

@router.get("", response_model=list[dict])
async def list_user_dashboards(
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> list[dict]:
    repo = DashboardRepository(db)
    dashboards = await repo.get_by_owner_id(user.id)
    return [
        {"id": str(d.id), "name": d.name, "type": d.type}
        for d in dashboards
    ]

@router.post("", status_code=201)
async def create_new_dashboard(
    name: str,
    type: str = "personal",
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    repo = DashboardRepository(db)
    dashboard = DbDashboard(
        name=name,
        type=type,
        owner_id=user.id
    )
    await repo.create(dashboard)
    return {"status": "created", "dashboard_id": str(dashboard.id)}

from typing import Any
