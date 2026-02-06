from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.core.database import engine
from sqlmodel import select
from src.models.user import User, UserCreate, UserLogin
from src.services.user_service import UserService
from src.core.security import create_access_token
from datetime import timedelta
from src.core.config import settings
from typing import Dict


router = APIRouter()


# Dependency to get database session
async def get_async_session():
    async with engine.begin() as conn:
        session = AsyncSession(conn)
        try:
            yield session
        finally:
            await session.close()


@router.post("/register", response_model=User)
async def register_user(user_create: UserCreate, db_session: AsyncSession = Depends(get_async_session)):
    # Check if user already exists
    existing_user = await UserService.get_user_by_email(email=user_create.email, db_session=db_session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create the user
    user = await UserService.create_user(user_create=user_create, db_session=db_session)
    return user


@router.post("/login")
async def login_user(user_login: UserLogin, db_session: AsyncSession = Depends(get_async_session)):
    user = await UserService.authenticate_user(
        email=user_login.email, 
        password=user_login.password, 
        db_session=db_session
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires  # Changed to use user.id instead of email
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout_user():
    # In a stateless JWT system, the server doesn't store session info
    # The client is responsible for removing the token from its storage
    return {"message": "Logged out successfully"}