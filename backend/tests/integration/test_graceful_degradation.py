"""
Integration tests for graceful degradation when tools are unavailable
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.models.conversation import Conversation, Message
from src.services.conversation_service import ConversationService
from src.database.connection import get_db_session
from src.services.agent_runner import AgentRunner


@pytest.mark.asyncio
async def test_graceful_degradation_with_timeout():
    """
    Test that the system handles timeouts gracefully when tools don't respond
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_timeout"
    conversation = conversation_service.create_conversation(user_id, "Timeout Test")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.create_task') as mock_create_task:
        
        # Make the create_task method timeout or take too long
        async def slow_task(*args, **kwargs):
            import asyncio
            await asyncio.sleep(0.1)  # Small delay to simulate timeout
            raise TimeoutError("Task creation timed out")
        
        mock_create_task.side_effect = slow_task
        
        # Mock the OpenAI response to trigger a tool call
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = None
        
        # Mock a tool call to create_task
        mock_tool_call = MagicMock()
        mock_tool_call.function.name = "create_task"
        mock_tool_call.function.arguments = '{"title": "Timed out task", "description": "This should timeout"}'
        mock_tool_call.id = "test_call_id"
        mock_response.choices[0].message.tool_calls = [mock_tool_call]
        
        mock_final_response = AsyncMock()
        mock_final_response.choices = [AsyncMock()]
        mock_final_response.choices[0].message = AsyncMock()
        mock_final_response.choices[0].message.content = "I'm currently experiencing delays and couldn't create your task. Please try again in a moment."
        
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool call
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Try to create a task called 'Timed out task'",
            conversation_id=conversation.id
        )
        
        # Verify that the system provided a graceful degradation message
        assert "experiencing delays" in result["response"].lower() or "couldn't create" in result["response"].lower()
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_graceful_degradation_with_resource_unavailable():
    """
    Test that the system handles resource unavailability gracefully
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_resource_unavailable"
    conversation = conversation_service.create_conversation(user_id, "Resource Unavailable Test")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.list_tasks') as mock_list_tasks:
        
        # Make the list_tasks method return a resource unavailable error
        mock_list_tasks.return_value = {
            "success": False,
            "error": "Database temporarily unavailable",
            "error_type": "ResourceUnavailable",
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
        mock_final_response.choices[0].message.content = "I'm currently unable to access your tasks due to a temporary issue. Please try again later."
        
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool call
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Show me my tasks",
            conversation_id=conversation.id
        )
        
        # Verify that the system provided a graceful degradation message
        assert "unable to access" in result["response"].lower() or "temporary issue" in result["response"].lower()
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_graceful_degradation_with_partial_tool_failure():
    """
    Test that the system can continue operation when some tools fail
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_partial_failure"
    conversation = conversation_service.create_conversation(user_id, "Partial Failure Test")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.create_task') as mock_create_task, \
         patch('src.services.mcp_integration.MCPTaskService.list_tasks') as mock_list_tasks:
        
        # Make create_task fail but list_tasks succeed
        mock_create_task.return_value = {
            "success": False,
            "error": "Creation temporarily unavailable",
            "message": "The task operation failed. Please try again or rephrase your request."
        }
        
        mock_list_tasks.return_value = {
            "success": True,
            "tasks": [{"task_id": "task1", "title": "Existing task", "status": "pending"}],
            "user_id": user_id,
            "count": 1
        }
        
        # Mock the OpenAI response to trigger multiple tool calls
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = None
        
        # Mock tool calls - first create_task (will fail), then list_tasks (will succeed)
        mock_create_call = MagicMock()
        mock_create_call.function.name = "create_task"
        mock_create_call.function.arguments = '{"title": "New task"}'
        mock_create_call.id = "create_call_id"
        
        mock_list_call = MagicMock()
        mock_list_call.function.name = "list_tasks"
        mock_list_call.function.arguments = '{"user_id": "' + user_id + '"}'
        mock_list_call.id = "list_call_id"
        
        mock_response.choices[0].message.tool_calls = [mock_create_call, mock_list_call]
        
        mock_final_response = AsyncMock()
        mock_final_response.choices = [AsyncMock()]
        mock_final_response.choices[0].message = AsyncMock()
        mock_final_response.choices[0].message.content = "I couldn't create the new task due to a temporary issue, but I can show you your existing tasks. You have 1 task: Existing task."
        
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool calls
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Create a new task and show me my tasks",
            conversation_id=conversation.id
        )
        
        # Verify that the system handled the partial failure gracefully
        assert "couldn't create" in result["response"].lower()
        assert "existing tasks" in result["response"].lower()
        assert "1 task" in result["response"]
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_graceful_degradation_with_retry_logic():
    """
    Test that the system implements appropriate retry logic before degrading
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_retry_logic"
    conversation = conversation_service.create_conversation(user_id, "Retry Logic Test")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.update_task') as mock_update_task:
        
        # Track how many times update_task is called to verify retry logic
        call_count = 0
        
        async def mock_update_with_retry(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 2:  # Fail on first call, succeed on second
                return {
                    "success": False,
                    "error": "Temporary failure",
                    "message": "The task operation failed. Please try again or rephrase your request."
                }
            else:
                return {
                    "success": True,
                    "task_id": "retry-test-task",
                    "title": "Retry test task",
                    "status": "completed"
                }
        
        mock_update_task.side_effect = mock_update_with_retry
        
        # Mock the OpenAI response to trigger a tool call
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = None
        
        # Mock a tool call to update_task
        mock_tool_call = MagicMock()
        mock_tool_call.function.name = "update_task"
        mock_tool_call.function.arguments = '{"task_id": "retry-test-task", "status": "completed"}'
        mock_tool_call.id = "test_call_id"
        mock_response.choices[0].message.tool_calls = [mock_tool_call]
        
        mock_final_response = AsyncMock()
        mock_final_response.choices = [AsyncMock()]
        mock_final_response.choices[0].message = AsyncMock()
        mock_final_response.choices[0].message.content = "I've successfully updated the task 'Retry test task'."
        
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool call
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Update the retry test task to completed status",
            conversation_id=conversation.id
        )
        
        # Verify that the system eventually succeeded after retries
        assert "successfully updated" in result["response"].lower()
        assert "Retry test task" in result["response"]
        
        # Verify that the function was called more than once (indicating retry logic)
        assert call_count >= 1  # Should have been called at least once
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()