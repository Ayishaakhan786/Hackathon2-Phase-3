"""
Integration tests for conversation context preservation
"""
import pytest
from uuid import uuid4
from sqlmodel import Session
from unittest.mock import AsyncMock, patch

from src.models.conversation import Conversation, Message
from src.services.conversation_service import ConversationService
from src.database.connection import get_db_session


@pytest.mark.asyncio
async def test_conversation_context_preservation():
    """
    Test that conversation context is properly preserved across multiple interactions
    """
    # Create a test conversation with initial messages
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_123"
    conversation = conversation_service.create_conversation(user_id, "Test Conversation")
    
    # Add initial messages to establish context
    conversation_service.create_message(
        conversation.id,
        "user",
        "I want to create a task called 'Buy groceries'"
    )
    
    conversation_service.create_message(
        conversation.id,
        "assistant",
        "Sure, I've created the task 'Buy groceries' for you."
    )
    
    # Add another message
    conversation_service.create_message(
        conversation.id,
        "user",
        "Now add 'Milk' to my grocery list"
    )
    
    # Verify the context is built correctly
    context = conversation_service.build_conversation_context(conversation.id, limit=10)
    
    # Check that the context contains the expected messages
    assert len(context) >= 3  # At least the 3 messages we added
    
    # Check that the most recent messages are included
    user_messages = [msg for msg in context if msg["role"] == "user"]
    assistant_messages = [msg for msg in context if msg["role"] == "assistant"]
    
    assert len(user_messages) >= 2
    assert len(assistant_messages) >= 1
    
    # Verify that the context contains the expected content
    user_contents = [msg["content"] for msg in user_messages]
    assert "I want to create a task called 'Buy groceries'" in user_contents
    assert "Now add 'Milk' to my grocery list" in user_contents
    
    # Clean up
    db_session.delete(conversation)
    db_session.commit()


@pytest.mark.asyncio
async def test_conversation_resumption_after_interruption():
    """
    Test that conversation can be resumed after interruption
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_456"
    conversation = conversation_service.create_conversation(user_id, "Resume Test")
    
    # Add initial messages
    conversation_service.create_message(
        conversation.id,
        "user",
        "I have a task to remember: 'Complete the project proposal'"
    )
    
    conversation_service.create_message(
        conversation.id,
        "assistant",
        "Got it, I've noted the task 'Complete the project proposal'."
    )
    
    # Simulate interruption and resumption by creating a new service instance
    # (which simulates a new API request)
    new_conversation_service = ConversationService(db_session)
    
    # Resume conversation by adding a new message
    conversation_service.create_message(
        conversation.id,
        "user",
        "Can you remind me what my tasks were?"
    )
    
    # Build context for the resumed conversation
    context = new_conversation_service.build_conversation_context(conversation.id, limit=10)
    
    # Verify that the context includes the earlier conversation
    context_contents = [msg["content"] for msg in context]
    assert "I have a task to remember: 'Complete the project proposal'" in context_contents
    assert "Got it, I've noted the task 'Complete the project proposal'." in context_contents
    assert "Can you remind me what my tasks were?" in context_contents
    
    # Clean up
    db_session.delete(conversation)
    db_session.commit()


@pytest.mark.asyncio
async def test_context_passed_to_agent_across_requests():
    """
    Test that context is properly passed to agent across requests
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_789"
    conversation = conversation_service.create_conversation(user_id, "Context Test")
    
    # Add initial messages
    conversation_service.create_message(
        conversation.id,
        "user",
        "I'm planning a trip to Paris next week"
    )
    
    conversation_service.create_message(
        conversation.id,
        "assistant",
        "That sounds exciting! Are you planning activities for your trip?"
    )
    
    # Mock the agent runner to verify context is passed correctly
    with patch('src.services.agent_runner.client') as mock_openai:
        # Mock the response from OpenAI
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = "Yes, I'd love to hear about your plans for Paris!"
        mock_response.choices[0].message.tool_calls = None
        
        mock_openai.chat.completions.create.return_value = mock_response
        
        from src.services.agent_runner import AgentRunner
        
        # Create agent runner and run with context
        agent_runner = AgentRunner(db_session)
        
        # Run the agent with a follow-up message
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Yes, I want to visit the Eiffel Tower and Louvre Museum",
            conversation_id=conversation.id
        )
        
        # Verify the conversation was updated with the new message
        messages = conversation_service.get_messages_by_conversation(conversation.id)
        user_messages = [msg for msg in messages if msg.role == "user"]
        
        # Should have the original message and the new one
        user_contents = [msg.content for msg in user_messages]
        assert "I'm planning a trip to Paris next week" in user_contents
        assert "Yes, I want to visit the Eiffel Tower and Louvre Museum" in user_contents
        
        # Verify the OpenAI call was made with the correct context
        # (the call_args should include the conversation history)
        call_args = mock_openai.chat.completions.create.call_args
        messages_sent = call_args[1]['messages']
        
        # Check that system message and conversation history are included
        role_contents = [(msg['role'], msg['content']) for msg in messages_sent]
        assert ('system', 'You are a helpful assistant that helps users manage their tasks using natural language.') in role_contents
        assert ('user', 'I\'m planning a trip to Paris next week') in role_contents
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()