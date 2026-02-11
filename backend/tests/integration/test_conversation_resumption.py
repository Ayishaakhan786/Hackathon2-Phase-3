"""
Integration tests for conversation resumption after interruption
"""
import pytest
from uuid import uuid4
from sqlmodel import Session

from src.models.conversation import Conversation, Message
from src.services.conversation_service import ConversationService
from src.database.connection import get_db_session


@pytest.mark.asyncio
async def test_conversation_resumption_with_new_session():
    """
    Test that conversation can be resumed with a new database session
    """
    # Create initial session and conversation
    initial_session = next(get_db_session())
    conversation_service = ConversationService(initial_session)
    
    user_id = "test_user_resumption"
    conversation = conversation_service.create_conversation(user_id, "Resumption Test")
    
    # Add initial messages
    conversation_service.create_message(
        conversation.id,
        "user",
        "I need to schedule a meeting with my team tomorrow"
    )
    
    conversation_service.create_message(
        conversation.id,
        "assistant",
        "Sure, I've scheduled a meeting with your team for tomorrow."
    )
    
    # Close the initial session (simulating request completion)
    initial_session.close()
    
    # Create a new session (simulating a new API request)
    new_session = next(get_db_session())
    new_conversation_service = ConversationService(new_session)
    
    # Resume the conversation with a follow-up
    conversation_service.create_message(
        conversation.id,
        "user",
        "What time is the meeting?"
    )
    
    # Verify the conversation context is preserved
    full_history = new_conversation_service.get_full_conversation_history(conversation.id)
    user_messages = [msg for msg in full_history if msg.role == "user"]
    assistant_messages = [msg for msg in full_history if msg.role == "assistant"]
    
    assert len(user_messages) == 2  # Original + follow-up
    assert len(assistant_messages) == 1  # Original response
    
    # Verify the content is preserved
    contents = [msg.content for msg in user_messages]
    assert "I need to schedule a meeting with my team tomorrow" in contents
    assert "What time is the meeting?" in contents
    
    # Clean up
    new_session.delete(conversation)
    new_session.commit()
    new_session.close()


@pytest.mark.asyncio
async def test_conversation_resumption_with_different_conversation_ids():
    """
    Test that conversation can be resumed using the conversation ID
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    user_id = "test_user_different_session"
    
    # Create conversation in one "session"
    conversation = conversation_service.create_conversation(user_id, "Different Session Test")
    
    # Add initial messages
    conversation_service.create_message(
        conversation.id,
        "user",
        "Create a task to water the plants"
    )
    
    conversation_service.create_message(
        conversation.id,
        "assistant",
        "I've created the task 'water the plants'."
    )
    
    # Simulate a new "session" by creating a fresh service instance with same session
    # but acting as if we're starting fresh with just the conversation ID
    fresh_conversation_service = ConversationService(db_session)
    
    # Resume using the conversation ID
    resumed_conversation = fresh_conversation_service.get_conversation_by_id(conversation.id)
    assert resumed_conversation is not None
    assert resumed_conversation.user_id == user_id
    
    # Add a follow-up message in the resumed context
    conversation_service.create_message(
        conversation.id,
        "user",
        "Did you complete the watering task?"
    )
    
    # Verify the full context is available
    all_messages = fresh_conversation_service.get_full_conversation_history(conversation.id)
    assert len(all_messages) == 3  # Two original + one follow-up
    
    # Verify message order and content
    contents = [msg.content for msg in all_messages]
    assert "Create a task to water the plants" in contents
    assert "I've created the task 'water the plants'." in contents
    assert "Did you complete the watering task?" in contents
    
    # Clean up
    db_session.delete(conversation)
    db_session.commit()


@pytest.mark.asyncio
async def test_conversation_state_preservation_after_interruption():
    """
    Test that conversation state is preserved after interruption
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    user_id = "test_user_state_preservation"
    
    # Create conversation
    conversation = conversation_service.create_conversation(user_id, "State Preservation Test")
    
    # Add messages establishing context
    conversation_service.create_message(
        conversation.id,
        "user",
        "I'm working on a project called 'Website Redesign'"
    )
    
    conversation_service.create_message(
        conversation.id,
        "assistant",
        "Great! What aspects of the website redesign are you focusing on?"
    )
    
    # Get initial summary
    initial_summary = conversation_service.get_conversation_summary(conversation.id)
    
    # Simulate interruption by creating a new service instance
    new_conversation_service = ConversationService(db_session)
    
    # Add follow-up message
    conversation_service.create_message(
        conversation.id,
        "user",
        "I'm focusing on the homepage layout and navigation"
    )
    
    # Get updated summary after resumption
    updated_summary = new_conversation_service.get_conversation_summary(conversation.id)
    
    # Verify conversation properties are preserved and updated correctly
    assert updated_summary["id"] == str(conversation.id)
    assert updated_summary["user_id"] == user_id
    assert updated_summary["title"] == "State Preservation Test"
    assert updated_summary["total_messages"] == 3  # 2 original + 1 follow-up
    assert updated_summary["user_messages_count"] == 2
    assert updated_summary["assistant_messages_count"] == 1
    
    # Verify the updated_at timestamp has changed
    assert updated_summary["updated_at"] is not None
    
    # Clean up
    db_session.delete(conversation)
    db_session.commit()