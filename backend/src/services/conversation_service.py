from typing import List, Optional, Dict, Any
from sqlmodel import Session
from uuid import UUID
from ..models.conversation import Conversation
from ..models.message import Message
from ..database.crud_optimized import (
    create_conversation as crud_create_conversation,
    get_conversation_by_id as crud_get_conversation_by_id,
    get_conversations_by_user as crud_get_conversations_by_user,
    update_conversation_title as crud_update_conversation_title,
    delete_conversation as crud_delete_conversation,
    create_message as crud_create_message,
    get_message_by_id as crud_get_message_by_id,
    get_messages_by_conversation as crud_get_messages_by_conversation,
    get_latest_messages_by_conversation as crud_get_latest_messages_by_conversation,
    delete_message as crud_delete_message,
    get_conversation_with_messages as crud_get_conversation_with_messages,
    get_conversation_summary as crud_get_conversation_summary,
    get_messages_by_conversation_optimized as crud_get_messages_by_conversation_optimized
)


class ConversationService:
    """
    Service class to handle conversation-related business logic
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create_conversation(self, user_id: str, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation
        """
        return crud_create_conversation(self.db_session, user_id, title)
    
    def get_conversation_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """
        Retrieve a conversation by its ID
        """
        return crud_get_conversation_by_id(self.db_session, conversation_id)
    
    def get_conversations_by_user(self, user_id: str) -> List[Conversation]:
        """
        Retrieve all conversations for a specific user
        """
        return crud_get_conversations_by_user(self.db_session, user_id)
    
    def update_conversation_title(self, conversation_id: UUID, title: str) -> Optional[Conversation]:
        """
        Update the title of a conversation
        """
        return crud_update_conversation_title(self.db_session, conversation_id, title)
    
    def delete_conversation(self, conversation_id: UUID) -> bool:
        """
        Delete a conversation by its ID
        """
        return crud_delete_conversation(self.db_session, conversation_id)
    
    def create_message(
        self, 
        conversation_id: UUID, 
        role: str, 
        content: str, 
        metadata: Optional[dict] = None
    ) -> Message:
        """
        Create a new message in a conversation
        """
        return crud_create_message(
            self.db_session, 
            conversation_id, 
            role, 
            content, 
            metadata
        )
    
    def get_message_by_id(self, message_id: UUID) -> Optional[Message]:
        """
        Retrieve a message by its ID
        """
        return crud_get_message_by_id(self.db_session, message_id)
    
    def get_messages_by_conversation(
        self, 
        conversation_id: UUID, 
        offset: int = 0, 
        limit: int = 100
    ) -> List[Message]:
        """
        Retrieve messages for a specific conversation with pagination
        """
        return crud_get_messages_by_conversation(
            self.db_session, 
            conversation_id, 
            offset, 
            limit
        )
    
    def get_latest_messages_by_conversation(
        self, 
        conversation_id: UUID, 
        limit: int = 10
    ) -> List[Message]:
        """
        Retrieve the latest messages for a specific conversation
        """
        return crud_get_latest_messages_by_conversation(
            self.db_session, 
            conversation_id, 
            limit
        )
    
    def delete_message(self, message_id: UUID) -> bool:
        """
        Delete a message by its ID
        """
        return crud_delete_message(self.db_session, message_id)
    
    def build_conversation_context(self, conversation_id: UUID, limit: int = 20) -> List[dict]:
        """
        Build conversation context for the AI agent with the latest messages
        """
        messages = self.get_latest_messages_by_conversation(conversation_id, limit)
        context = []
        for msg in messages:
            context.append({
                "role": msg.role,
                "content": msg.content
            })
        return context
    
    def get_full_conversation_history(self, conversation_id: UUID) -> List[Message]:
        """
        Retrieve the full conversation history for a given conversation
        """
        # Use the optimized function to get messages
        return crud_get_messages_by_conversation_optimized(
            self.db_session,
            conversation_id,
            limit=1000  # Adjust limit as needed
        )
    
    def get_conversation_summary(self, conversation_id: UUID) -> Dict[str, Any]:
        """
        Get a summary of the conversation including metadata using optimized query
        """
        # Use the optimized function that gets summary in a single query
        summary = crud_get_conversation_summary(self.db_session, conversation_id)
        if not summary:
            return {}
        
        # Convert datetime objects to ISO format strings
        result = {**summary}
        if result["created_at"]:
            result["created_at"] = result["created_at"].isoformat()
        if result["updated_at"]:
            result["updated_at"] = result["updated_at"].isoformat()
        if result["last_message_time"]:
            result["last_message_time"] = result["last_message_time"].isoformat()
        
        # Rename some fields to match the expected format
        result["user_messages_count"] = result.pop("user_messages", 0)
        result["assistant_messages_count"] = result.pop("assistant_messages", 0)
        result["last_message_timestamp"] = result.pop("last_message_time", None)
        
        return result

    def update_conversation_state(self, conversation_id: UUID, state: str) -> Optional[Conversation]:
        """
        Update the state of a conversation (active, archived, etc.)
        """
        from sqlalchemy import func
        conversation = self.db_session.get(Conversation, conversation_id)
        if conversation:
            # In a real implementation, you might have a specific field for state
            # For now, we'll update the updated_at timestamp to show activity
            conversation.updated_at = func.now()
            self.db_session.add(conversation)
            self.db_session.commit()
            self.db_session.refresh(conversation)
        return conversation