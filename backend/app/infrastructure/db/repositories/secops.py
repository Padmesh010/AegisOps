import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.secops import DbSecurityScan, DbScanFinding, DbSBOMRecord
from app.infrastructure.db.repositories.base import BaseRepository

class SecurityScanRepository(BaseRepository[DbSecurityScan]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbSecurityScan, session)

    async def get_by_target(self, target_path: str) -> List[DbSecurityScan]:
        result = await self.session.execute(
            select(self.model).where(self.model.target_path == target_path)
        )
        return list(result.scalars().all())

class ScanFindingRepository(BaseRepository[DbScanFinding]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbScanFinding, session)

    async def get_by_scan_id(self, scan_id: uuid.UUID) -> List[DbScanFinding]:
        result = await self.session.execute(
            select(self.model).where(self.model.scan_id == scan_id)
        )
        return list(result.scalars().all())
