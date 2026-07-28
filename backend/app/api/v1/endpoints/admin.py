from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.api.dependencies import RequirePermission, get_db_session
from app.infrastructure.db.models.user import User, Role, Permission
from app.api.v1.endpoints.auth import UserResponse

router = APIRouter()

class CreateRoleRequest(BaseModel):
    name: str
    description: str

class RoleResponse(BaseModel):
    id: str
    name: str
    description: str

@router.get("/users", response_model=List[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db_session),
    admin: Any = Depends(RequirePermission("admin"))
) -> List[UserResponse]:
    """Fetch all users in the system (Admin only)."""
    result = await db.execute(select(User).where(User.is_deleted == False))
    users = result.scalars().all()
    return [
        UserResponse(
            id=str(u.id),
            email=u.email,
            username=u.username,
            status=u.status
        ) for u in users
    ]

@router.post("/roles", response_model=RoleResponse, status_code=201)
async def create_role(
    req: CreateRoleRequest,
    db: AsyncSession = Depends(get_db_session),
    admin: Any = Depends(RequirePermission("admin"))
) -> RoleResponse:
    """Create a new security Role (Admin only)."""
    new_role = Role(name=req.name, description=req.description)
    db.add(new_role)
    await db.flush()
    return RoleResponse(
        id=str(new_role.id),
        name=new_role.name,
        description=new_role.description or ""
    )

from typing import Any
