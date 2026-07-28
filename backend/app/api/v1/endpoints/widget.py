from fastapi import APIRouter, Depends, HTTPException
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.dashboard import DbWidget
from app.services.dashboard.engine import layout_engine

router = APIRouter()

@router.post("/{dashboard_id}", status_code=201)
async def add_widget_to_dashboard(
    dashboard_id: str,
    title: str,
    widget_type: str,
    layout: dict,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    if not layout_engine.validate_layout_grid(layout):
        raise HTTPException(status_code=400, detail="Invalid widget layout dimensions.")
        
    widget = DbWidget(
        dashboard_id=uuid.UUID(dashboard_id),
        title=title,
        type=widget_type,
        grid_layout=layout
    )
    db.add(widget)
    await db.commit()
    return {"status": "added", "widget_id": str(widget.id)}

from typing import Any
