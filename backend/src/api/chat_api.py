from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from sqlmodel import Session
from pydantic import BaseModel
import logging
import uuid

from ..models.conversation import ConversationRead
from ..models.message import MessageRead
from ..api.deps import get_sync_session
from ..services.conversation_service import ConversationService
from ..services.message_service import save_message, fetch_conversation_history, fetch_formatted_conversation_history
import logging

router = APIRouter(prefix="/api/{user_id}", tags=["chat"])

# Pydantic models for request/response
class ChatRequest(BaseModel):
    conversation_id: str = None  # Optional: if not provided, create new conversation
    message: str  # Required: user's message content


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[Dict[str, Any]] = []  # Empty for now, reserved for future AI agent integration


@router.post("/chat", response_model=ChatResponse)
def chat(
    user_id: str,
    chat_request: ChatRequest,
    session: Session = Depends(get_sync_session)
) -> ChatResponse:
    """
    Main chat endpoint that handles both new conversations and existing ones.

    If no conversation_id is provided, creates a new conversation.
    Saves the user's message and generates a placeholder assistant response.
    Saves the assistant's response and returns the conversation ID and response.
    """
    conversation_id = chat_request.conversation_id

    # Create conversation service instance
    conversation_service = ConversationService(session)

    # Convert conversation_id to UUID if it exists
    conversation_uuid = None
    if conversation_id:
        try:
            conversation_uuid = uuid.UUID(conversation_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")

    # Get or create conversation
    if conversation_uuid:
        # Verify conversation exists and belongs to user
        try:
            conversation = conversation_service.get_conversation_by_id(
                conversation_id=conversation_uuid
            )
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(status_code=404, detail="Conversation not found or doesn't belong to user")
        except Exception as e:
            logging.error(f"Error retrieving conversation {conversation_uuid} for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error while retrieving conversation")
    else:
        # Create new conversation
        try:
            conversation = conversation_service.create_conversation(user_id=user_id)
            conversation_uuid = conversation.id
            conversation_id = str(conversation.id)
        except Exception as e:
            logging.error(f"Error creating conversation for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error while creating conversation")

    # Save user message
    try:
        user_message = save_message(
            session=session,
            conversation_id=conversation_uuid,
            role="user",
            content=chat_request.message
        )
    except Exception as e:
        logging.error(f"Error saving user message for conversation {conversation_uuid}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while saving message")

    # Generate placeholder assistant response
    # In a real implementation, this would connect to an AI agent
    assistant_response = f"I received your message: '{chat_request.message}'. This is a placeholder response."

    # Save assistant response
    try:
        assistant_message = save_message(
            session=session,
            conversation_id=conversation_uuid,
            role="assistant",
            content=assistant_response
        )
    except Exception as e:
        logging.error(f"Error saving assistant response for conversation {conversation_uuid}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while saving assistant response")

    return ChatResponse(
        conversation_id=conversation_id,
        response=assistant_response,
        tool_calls=[]
    )