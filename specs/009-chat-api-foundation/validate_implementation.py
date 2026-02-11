"""
Quick validation script to test the chat API functionality
"""
import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src'))

from sqlmodel import SQLModel
from src.database.connection import engine, get_session
from src.models.conversation import Conversation
from src.models.message import Message
from src.services.conversation_service import create_conversation, get_conversation
from src.services.message_service import save_message, fetch_conversation_history


def validate_implementation():
    """Validate that the basic functionality works as expected"""
    print("Validating Chat API Foundation implementation...")
    
    # Create tables
    SQLModel.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    # Test conversation creation
    with next(get_session()) as session:
        user_id = "test_user_123"
        
        # Create a conversation
        conversation = create_conversation(session=session, user_id=user_id)
        print(f"✓ Conversation created with ID: {conversation.id}")
        
        # Verify conversation exists and belongs to user
        retrieved_conversation = get_conversation(
            session=session,
            conversation_id=conversation.id,
            user_id=user_id
        )
        assert retrieved_conversation is not None
        assert retrieved_conversation.user_id == user_id
        print("✓ Conversation retrieval and user validation working")
        
        # Save a user message
        user_message = save_message(
            session=session,
            user_id=user_id,
            conversation_id=conversation.id,
            role="user",
            content="Hello, this is a test message!"
        )
        print("✓ User message saved successfully")
        
        # Save an assistant response
        assistant_message = save_message(
            session=session,
            user_id=user_id,  # Using same user ID for simplicity in test
            conversation_id=conversation.id,
            role="assistant",
            content="This is a placeholder assistant response."
        )
        print("✓ Assistant response saved successfully")
        
        # Fetch conversation history
        history = fetch_conversation_history(
            session=session,
            conversation_id=conversation.id
        )
        assert len(history) >= 2  # At least user message and assistant response
        print(f"✓ Conversation history retrieved with {len(history)} messages")
        
        # Verify message roles are correct
        user_messages = [msg for msg in history if msg.role == "user"]
        assistant_messages = [msg for msg in history if msg.role == "assistant"]
        assert len(user_messages) >= 1
        assert len(assistant_messages) >= 1
        print("✓ Message roles are correctly stored and retrieved")
    
    print("\n✓ All validations passed! Chat API Foundation implementation is working correctly.")
    

if __name__ == "__main__":
    validate_implementation()