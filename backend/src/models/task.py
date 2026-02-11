from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    user_id: str
    status: str = "pending"  # Default status is pending


class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())