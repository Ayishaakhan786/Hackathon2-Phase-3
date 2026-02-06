from sqlmodel import SQLModel, Field, Column, DateTime, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .user import User


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime, nullable=False, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow))
    
    # Foreign key to User
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    
    # Relationship to User
    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    title: str
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None


class TaskRead(TaskBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID