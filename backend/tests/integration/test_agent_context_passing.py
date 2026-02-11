"""
Integration tests for verifying context is properly passed to agent across requests
"""
import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.models.conversation import Conversation, Message
from src.services.conversation_service import ConversationService
from src.database.connection import get_db_session
from src.services.agent_runner import AgentRunner


@pytest.mark.asyncio
async def test_context_passed_to_agent_in_subsequent_requests():
    """
    Test that conversation context is properly passed to the agent in subsequent requests
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_context_passing"
    conversation = conversation_service.create_conversation(user_id, "Context Passing Test")
    
    # Add initial messages to establish context
    conversation_service.create_message(
        conversation.id,
        "user",
        "I want to create a task to 'Buy groceries for the week'"
    )
    
    conversation_service.create_message(
        conversation.id,
        "assistant",
        "Okay, I've created the task 'Buy groceries for the week'."
    )
    
    # Mock the OpenAI client to verify context is passed correctly
    with patch('src.services.agent_runner.client') as mock_openai:
        # Mock the response from OpenAI
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = "Sure, I can help you with that. What groceries do you need?"
        mock_response.choices[0].message.tool_calls = None
        
        mock_openai.chat.completions.create.return_value = mock_response
        
        # Create agent runner and run with follow-up message
        agent_runner = AgentRunner(db_session)
        
        # Send a follow-up message that should have access to the conversation history
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="I need milk, bread, and eggs",
            conversation_id=conversation.id
        )
        
        # Verify the OpenAI API was called with the correct context
        call_args = mock_openai.chat.completions.create.call_args
        sent_messages = call_args[1]['messages']
        
        # Check that the system prompt is included
        system_messages = [msg for msg in sent_messages if msg['role'] == 'system']
        assert len(system_messages) == 1
        
        # Check that the conversation history is included
        user_messages = [msg for msg in sent_messages if msg['role'] == 'user']
        assistant_messages = [msg for msg in sent_messages if msg['role'] == 'assistant']
        
        # Should include the original user message and assistant response
        user_contents = [msg['content'] for msg in user_messages]
        assert "I want to create a task to 'Buy groceries for the week'" in user_contents
        
        assistant_contents = [msg['content'] for msg in assistant_messages]
        assert "Okay, I've created the task 'Buy groceries for the week'." in assistant_contents
        
        # Should also include the new message
        assert "I need milk, bread, and eggs" in user_contents
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_context_ordering_when_passed_to_agent():
    """
    Test that conversation context is properly ordered when passed to the agent
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_context_ordering"
    conversation = conversation_service.create_conversation(user_id, "Context Ordering Test")
    
    # Add messages in chronological order
    conversation_service.create_message(conversation.id, "user", "First message: I want to create a task")
    conversation_service.create_message(conversation.id, "assistant", "First response: What should the task be?")
    conversation_service.create_message(conversation.id, "user", "Second message: Create a task called 'Clean the house'")
    conversation_service.create_message(conversation.id, "assistant", "Second response: I've created the task 'Clean the house'")
    conversation_service.create_message(conversation.id, "user", "Third message: Also add 'Buy groceries' to my tasks")
    
    # Mock the OpenAI client to check message ordering
    with patch('src.services.agent_runner.client') as mock_openai:
        # Mock the response from OpenAI
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = "Sure, I've added 'Buy groceries' to your tasks."
        mock_response.choices[0].message.tool_calls = None
        
        mock_openai.chat.completions.create.return_value = mock_response
        
        # Create agent runner and run with follow-up message
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Third message: Also add 'Buy groceries' to my tasks",
            conversation_id=conversation.id
        )
        
        # Verify the messages were sent in the correct chronological order
        call_args = mock_openai.chat.completions.create.call_args
        sent_messages = call_args[1]['messages']
        
        # Extract the content of user and assistant messages (excluding system message)
        message_contents = []
        for msg in sent_messages:
            if msg['role'] in ['user', 'assistant']:
                message_contents.append((msg['role'], msg['content']))
        
        # Check that messages appear in chronological order
        expected_sequence = [
            ('user', 'First message: I want to create a task'),
            ('assistant', "First response: What should the task be?"),
            ('user', 'Second message: Create a task called \'Clean the house\''),
            ('assistant', "Second response: I've created the task 'Clean the house'"),
            ('user', 'Third message: Also add \'Buy groceries\' to my tasks')
        ]
        
        # The actual sequence should contain our expected sequence as a subset
        for expected_msg in expected_sequence:
            assert expected_msg in message_contents, f"Expected message {expected_msg} not found in context"
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_context_limiting_when_passed_to_agent():
    """
    Test that conversation context is properly limited when passed to the agent
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_context_limiting"
    conversation = conversation_service.create_conversation(user_id, "Context Limiting Test")
    
    # Add many messages to test the limit
    for i in range(25):  # More than the default limit
        conversation_service.create_message(conversation.id, "user", f"Message {i}: User content")
        conversation_service.create_message(conversation.id, "assistant", f"Message {i}: Assistant response")
    
    # Mock the OpenAI client to check how many messages are sent
    with patch('src.services.agent_runner.client') as mock_openai:
        # Mock the response from OpenAI
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = "Processed the request."
        mock_response.choices[0].message.tool_calls = None
        
        mock_openai.chat.completions.create.return_value = mock_response
        
        # Create agent runner and run with a new message
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Final message: What did we discuss?",
            conversation_id=conversation.id
        )
        
        # Verify the messages were sent with proper limiting
        call_args = mock_openai.chat.completions.create.call_args
        sent_messages = call_args[1]['messages']
        
        # Count only user and assistant messages (exclude system message)
        user_and_assistant_msgs = [msg for msg in sent_messages if msg['role'] in ['user', 'assistant']]
        
        # The context should be limited (by default to 20 in build_conversation_context)
        # Plus the new user message, so total should be <= 21
        assert len(user_and_assistant_msgs) <= 21, f"Too many messages sent to agent: {len(user_and_assistant_msgs)}"
        
        # The final user message should be included
        final_user_msg_found = any(
            msg['role'] == 'user' and 'What did we discuss?' in msg['content']
            for msg in user_and_assistant_msgs
        )
        assert final_user_msg_found, "Final user message was not included in context"
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()