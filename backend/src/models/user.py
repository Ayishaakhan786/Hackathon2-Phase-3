from sqlmodel import SQLModel, Field, Column, DateTime, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)


class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime, nullable=False, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow))
    
    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserLogin(SQLModel):
    email: str
    password: str