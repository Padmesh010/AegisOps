from typing import Any, Generic, List, Optional, Type, TypeVar, Union
import uuid
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get(self, id: Union[uuid.UUID, str]) -> Optional[ModelType]:
        """Fetch a single record by its UUID primary key."""
        if isinstance(id, str):
            parsed_id = uuid.UUID(id)
        else:
            parsed_id = id
        
        result = await self.session.execute(
            select(self.model).where(self.model.id == parsed_id)  # type: ignore
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None,
        sort_desc: bool = False
    ) -> List[ModelType]:
        """Fetch multiple records with pagination, filtering, and sorting."""
        query = select(self.model)
        
        # Apply Sorting
        if sort_by and hasattr(self.model, sort_by):
            sort_attr = getattr(self.model, sort_by)
            if sort_desc:
                query = query.order_by(sort_attr.desc())
            else:
                query = query.order_by(sort_attr.asc())
        
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, obj_in: ModelType) -> ModelType:
        """Persist a new entity record."""
        self.session.add(obj_in)
        await self.session.flush()
        return obj_in

    async def update(self, db_obj: ModelType, update_data: dict[str, Any]) -> ModelType:
        """Modify fields on an existing database entity record."""
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def remove(self, id: Union[uuid.UUID, str]) -> Optional[ModelType]:
        """Remove a record by its UUID primary key."""
        obj = await self.get(id)
        if obj:
            # Handle Soft Delete Mixin support
            if hasattr(obj, "is_deleted"):
                setattr(obj, "is_deleted", True)
                from app.utils.time import get_utc_now
                setattr(obj, "deleted_at", get_utc_now())
                self.session.add(obj)
            else:
                await self.session.delete(obj)
            await self.session.flush()
        return obj
