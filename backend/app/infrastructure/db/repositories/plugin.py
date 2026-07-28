import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.plugin import DbPlugin, DbPluginVersion
from app.infrastructure.db.repositories.base import BaseRepository

class PluginRepository(BaseRepository[DbPlugin]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbPlugin, session)

    async def get_by_plugin_id(self, plugin_id: str) -> Optional[DbPlugin]:
        result = await self.session.execute(
            select(self.model).where(self.model.plugin_id == plugin_id)
        )
        return result.scalar_one_or_none()

    async def get_active_plugins(self) -> List[DbPlugin]:
        result = await self.session.execute(
            select(self.model).where(self.model.is_active == True)
        )
        return list(result.scalars().all())
