"""
Integration tests for error handling scenarios with MCP tool failures
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4

from src.models.conversation import Conversation, Message
from src.services.conversation_service import ConversationService
from src.database.connection import get_db_session
from src.services.agent_runner import AgentRunner


@pytest.mark.asyncio
async def test_mcp_tool_failure_handling():
    """
    Test that MCP tool failures are properly handled and reported to the user
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_error_handling"
    conversation = conversation_service.create_conversation(user_id, "Error Handling Test")
    
    # Mock the OpenAI client and make the MCP service fail
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.create_task') as mock_create_task:
        
        # Make the create_task method raise an exception
        mock_create_task.side_effect = Exception("Database connection failed")
        
        # Mock the OpenAI response to trigger a tool call
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = None
        
        # Mock a tool call to create_task
        mock_tool_call = MagicMock()
        mock_tool_call.function.name = "create_task"
        mock_tool_call.function.arguments = '{"title": "Test Task", "description": "Test Description"}'
        mock_tool_call.id = "test_call_id"
        mock_response.choices[0].message.tool_calls = [mock_tool_call]
        
        mock_final_response = AsyncMock()
        mock_final_response.choices = [AsyncMock()]
        mock_final_response.choices[0].message = AsyncMock()
        mock_final_response.choices[0].message.content = "I'm sorry, but I couldn't create the task due to a system error. Please try again later."
        
        # First call is for the initial response with tool calls
        # Second call is for the follow-up after tool execution
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool call
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Create a task called 'Test Task'",
            conversation_id=conversation.id
        )
        
        # Verify that the error was handled gracefully
        assert "couldn't create the task" in result["response"].lower()
        assert result["response"] != "Create a task called 'Test Task'"  # Should not be the raw input
        
        # Verify that the error message was saved to the conversation
        messages = conversation_service.get_messages_by_conversation(conversation.id)
        assistant_messages = [msg for msg in messages if msg.role == "assistant"]
        
        # Should have at least one assistant message with the error info
        error_found = any("couldn't create the task" in msg.content.lower() for msg in assistant_messages)
        assert error_found, "Error message was not saved to conversation"
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_mcp_tool_authentication_failure():
    """
    Test handling of MCP tool authentication failures
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_auth_failure"
    conversation = conversation_service.create_conversation(user_id, "Auth Failure Test")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.list_tasks') as mock_list_tasks:
        
        # Make the list_tasks method return an authentication error
        mock_list_tasks.return_value = {
            "success": False,
            "error": "Authentication failed",
            "error_type": "AuthenticationError",
            "function": "list_tasks",
            "message": "The task operation failed. Please try again or rephrase your request.",
            "details": {"timestamp": "2023-01-01T00:00:00Z"}
        }
        
        # Mock the OpenAI response to trigger a tool call
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = None
        
        # Mock a tool call to list_tasks
        mock_tool_call = MagicMock()
        mock_tool_call.function.name = "list_tasks"
        mock_tool_call.function.arguments = '{"user_id": "' + user_id + '"}'
        mock_tool_call.id = "test_call_id"
        mock_response.choices[0].message.tool_calls = [mock_tool_call]
        
        mock_final_response = AsyncMock()
        mock_final_response.choices = [AsyncMock()]
        mock_final_response.choices[0].message = AsyncMock()
        mock_final_response.choices[0].message.content = "I'm sorry, but I couldn't retrieve your tasks due to an authentication issue."
        
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool call
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Show me my tasks",
            conversation_id=conversation.id
        )
        
        # Verify that the authentication error was handled gracefully
        assert "authentication" in result["response"].lower() or "couldn't retrieve" in result["response"].lower()
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_graceful_degradation_when_tools_unavailable():
    """
    Test that the system degrades gracefully when tools are unavailable
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_degraded_mode"
    conversation = conversation_service.create_conversation(user_id, "Degraded Mode Test")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService') as mock_mcp_service_class:
        
        # Create a mock instance of the MCP service
        mock_mcp_instance = MagicMock()
        
        # Make all methods return errors
        mock_mcp_instance.create_task.return_value = {
            "success": False,
            "error": "Service temporarily unavailable",
            "message": "The task operation failed. Please try again or rephrase your request."
        }
        mock_mcp_instance.update_task.return_value = {
            "success": False,
            "error": "Service temporarily unavailable",
            "message": "The task operation failed. Please try again or rephrase your request."
        }
        mock_mcp_instance.delete_task.return_value = {
            "success": False,
            "error": "Service temporarily unavailable",
            "message": "The task operation failed. Please try again or rephrase your request."
        }
        mock_mcp_instance.list_tasks.return_value = {
            "success": False,
            "error": "Service temporarily unavailable",
            "message": "The task operation failed. Please try again or rephrase your request."
        }
        
        # Assign the mock instance to the class
        mock_mcp_service_class.return_value = mock_mcp_instance
        
        # Mock the OpenAI response to trigger a tool call
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = None
        
        # Mock a tool call to create_task
        mock_tool_call = MagicMock()
        mock_tool_call.function.name = "create_task"
        mock_tool_call.function.arguments = '{"title": "Test Task"}'
        mock_tool_call.id = "test_call_id"
        mock_response.choices[0].message.tool_calls = [mock_tool_call]
        
        mock_final_response = AsyncMock()
        mock_final_response.choices = [AsyncMock()]
        mock_final_response.choices[0].message = AsyncMock()
        mock_final_response.choices[0].message.content = "I'm currently experiencing technical difficulties and can't create tasks right now. Please try again later."
        
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool call
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Create a task called 'Test Task'",
            conversation_id=conversation.id
        )
        
        # Verify that the system provided a graceful degradation message
        assert "technical difficulties" in result["response"].lower() or "can't create" in result["response"].lower()
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()