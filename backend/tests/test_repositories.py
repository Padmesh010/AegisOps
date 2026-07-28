import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.user import User
from app.infrastructure.db.repositories.user import UserRepository

@pytest.mark.anyio
async def test_user_repository_crud_operations(db_session: AsyncSession) -> None:
    user_repo = UserRepository(db_session)
    
    # 1. Create User
    new_user = User(
        email="test_repo@aegisops.io",
        username="test_repo_user",
        hashed_password="securepasswordhash"
    )
    created_user = await user_repo.create(new_user)
    assert created_user.id is not None
    assert created_user.email == "test_repo@aegisops.io"
    
    # 2. Get User
    fetched_user = await user_repo.get(created_user.id)
    assert fetched_user is not None
    assert fetched_user.username == "test_repo_user"
    
    # 3. Fetch by Email
    user_by_email = await user_repo.get_by_email("test_repo@aegisops.io")
    assert user_by_email is not None
    assert user_by_email.id == created_user.id
    
    # 4. Update User
    updated_user = await user_repo.update(created_user, {"username": "updated_repo_user"})
    assert updated_user.username == "updated_repo_user"
    
    # 5. Soft Delete User
    await user_repo.remove(created_user.id)
    deleted_check = await user_repo.get(created_user.id)
    assert deleted_check.is_deleted is True
