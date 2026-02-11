from pydantic import BaseModel
from typing import Optional, List


class ChatRequest(BaseModel):
    """
    Request model for the chat endpoint
    """
    message: str
    conversation_id: Optional[str] = None
    metadata: Optional[dict] = None


class MessageContent(BaseModel):
    """
    Model for message content in the response
    """
    role: str
    content: str
    tool_calls: Optional[List[dict]] = None


class ChatResponse(BaseModel):
    """
    Response model for the chat endpoint
    """
    conversation_id: str
    message: MessageContent
    timestamp: str
    next_action: str = "continue"