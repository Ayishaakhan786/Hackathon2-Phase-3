from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class ChatLogBase(SQLModel):
    user_message: str
    conversation_id: Optional[str] = None


class ChatLog(ChatLogBase, table=True):
    """
    Chat log model that acts as both Pydantic schema and database table
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_message: str = Field(max_length=10000)
    ai_response: str = Field(max_length=10000)
    conversation_id: Optional[str] = Field(default=None, max_length=100)


class ChatLogCreate(ChatLogBase):
    """Schema for creating a new chat log"""
    pass


class ChatLogRead(ChatLogBase):
    """Schema for reading chat log data"""
    id: uuid.UUID
    timestamp: datetime
    conversation_id: Optional[str] = None