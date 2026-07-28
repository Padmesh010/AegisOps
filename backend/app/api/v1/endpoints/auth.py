from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.core.config import get_settings
from app.core.exceptions import AuthenticationError, ValidationError
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.infrastructure.db.models.user import User, UserSession
from app.infrastructure.db.repositories.user import UserRepository

router = APIRouter()
settings = get_settings()

class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    status: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    req: UserRegisterRequest,
    db: AsyncSession = Depends(get_db_session)
) -> UserResponse:
    user_repo = UserRepository(db)
    
    # Verify uniqueness
    existing_email = await user_repo.get_by_email(req.email)
    if existing_email:
        raise ValidationError("Email is already registered")
        
    existing_user = await user_repo.get_by_username(req.username)
    if existing_user:
        raise ValidationError("Username is already taken")

    # Hash and save
    hashed = get_password_hash(req.password)
    new_user = User(
        email=req.email,
        username=req.username,
        hashed_password=hashed
    )
    await user_repo.create(new_user)
    return UserResponse(
        id=str(new_user.id),
        email=new_user.email,
        username=new_user.username,
        status=new_user.status
    )

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session)
) -> TokenResponse:
    user_repo = UserRepository(db)
    user = await user_repo.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise AuthenticationError("Invalid username or password")
        
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    
    # Save session
    session_record = UserSession(
        user_id=user.id,
        refresh_token=refresh,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(session_record)
    
    return TokenResponse(access_token=access, refresh_token=refresh)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        status=current_user.status
    )

@router.post("/change-password", status_code=204)
async def change_password(
    req: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> None:
    if not verify_password(req.old_password, current_user.hashed_password):
        raise AuthenticationError("Invalid old password configuration")
    
    current_user.hashed_password = get_password_hash(req.new_password)
    db.add(current_user)

from datetime import datetime, timezone
