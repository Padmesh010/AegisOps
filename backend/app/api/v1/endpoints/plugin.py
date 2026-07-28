from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.plugin import DbPlugin
from app.services.plugin.runtime import plugin_runtime
from app.infrastructure.db.repositories.plugin import PluginRepository

router = APIRouter()

@router.get("", response_model=list[dict])
async def list_installed_plugins(
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> list[dict]:
    repo = PluginRepository(db)
    plugins = await repo.get_active_plugins()
    return [
        {"id": str(p.id), "plugin_id": p.plugin_id, "name": p.name, "active": p.is_active}
        for p in plugins
    ]

@router.post("/{plugin_id}/enable", response_model=dict)
async def enable_plugin(
    plugin_id: str,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    repo = PluginRepository(db)
    plugin = await repo.get_by_plugin_id(plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
        
    plugin.is_active = True
    db.add(plugin)
    await db.commit()
    
    # Load module dynamically
    plugin_runtime.load_plugin_module(plugin.plugin_id, "mock_entry_point")
    return {"status": "enabled", "plugin": plugin_id}

from typing import Any
