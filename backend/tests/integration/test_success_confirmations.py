"""
Integration tests for verifying success confirmations are properly formatted
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.models.conversation import Conversation, Message
from src.services.conversation_service import ConversationService
from src.database.connection import get_db_session
from src.services.agent_runner import AgentRunner
from src.services.response_formatter import format_task_operation_success


@pytest.mark.asyncio
async def test_success_confirmation_formatting_for_create_task():
    """
    Test that success confirmations for task creation are properly formatted
    """
    # Test the response formatter directly first
    task_data = {"title": "Buy groceries", "description": "Get milk and bread"}
    success_msg = format_task_operation_success("create", task_data)
    
    assert "Buy groceries" in success_msg
    assert "successfully created" in success_msg.lower()
    
    # Now test through the full integration
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_success_confirm"
    conversation = conversation_service.create_conversation(user_id, "Success Confirmation Test")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.create_task') as mock_create_task:
        
        # Mock successful task creation
        mock_create_task.return_value = {
            "success": True,
            "task_id": "test-task-id",
            "title": "Buy groceries",
            "description": "Get milk and bread",
            "user_id": user_id,
            "status": "pending"
        }
        
        # Mock the OpenAI response to trigger a tool call
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = None
        
        # Mock a tool call to create_task
        mock_tool_call = MagicMock()
        mock_tool_call.function.name = "create_task"
        mock_tool_call.function.arguments = '{"title": "Buy groceries", "description": "Get milk and bread"}'
        mock_tool_call.id = "test_call_id"
        mock_response.choices[0].message.tool_calls = [mock_tool_call]
        
        mock_final_response = AsyncMock()
        mock_final_response.choices = [AsyncMock()]
        mock_final_response.choices[0].message = AsyncMock()
        mock_final_response.choices[0].message.content = "I've successfully created the task 'Buy groceries'."
        
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool call
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Create a task called 'Buy groceries'",
            conversation_id=conversation.id
        )
        
        # Verify that the success confirmation is properly formatted
        assert "Buy groceries" in result["response"]
        assert "successfully" in result["response"].lower()
        
        # Verify that the success message was saved to the conversation
        messages = conversation_service.get_messages_by_conversation(conversation.id)
        assistant_messages = [msg for msg in messages if msg.role == "assistant"]
        
        success_found = any("Buy groceries" in msg.content and "successfully" in msg.content.lower() 
                           for msg in assistant_messages)
        assert success_found, "Success confirmation was not saved to conversation"
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_success_confirmation_formatting_for_update_task():
    """
    Test that success confirmations for task updates are properly formatted
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_update_confirm"
    conversation = conversation_service.create_conversation(user_id, "Update Confirmation Test")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.update_task') as mock_update_task:
        
        # Mock successful task update
        mock_update_task.return_value = {
            "success": True,
            "task_id": "test-task-id",
            "title": "Updated task title",
            "status": "completed"
        }
        
        # Mock the OpenAI response to trigger a tool call
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = None
        
        # Mock a tool call to update_task
        mock_tool_call = MagicMock()
        mock_tool_call.function.name = "update_task"
        mock_tool_call.function.arguments = '{"task_id": "test-task-id", "title": "Updated task title", "status": "completed"}'
        mock_tool_call.id = "test_call_id"
        mock_response.choices[0].message.tool_calls = [mock_tool_call]
        
        mock_final_response = AsyncMock()
        mock_final_response.choices = [AsyncMock()]
        mock_final_response.choices[0].message = AsyncMock()
        mock_final_response.choices[0].message.content = "I've successfully updated the task 'Updated task title'."
        
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool call
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Update the task to mark it as completed",
            conversation_id=conversation.id
        )
        
        # Verify that the success confirmation is properly formatted
        assert "Updated task title" in result["response"]
        assert "successfully" in result["response"].lower()
        assert "updated" in result["response"].lower()
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_success_confirmation_formatting_for_delete_task():
    """
    Test that success confirmations for task deletion are properly formatted
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_delete_confirm"
    conversation = conversation_service.create_conversation(user_id, "Delete Confirmation Test")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.delete_task') as mock_delete_task:
        
        # Mock successful task deletion
        mock_delete_task.return_value = {
            "success": True,
            "task_id": "test-task-id"
        }
        
        # Mock the OpenAI response to trigger a tool call
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = None
        
        # Mock a tool call to delete_task
        mock_tool_call = MagicMock()
        mock_tool_call.function.name = "delete_task"
        mock_tool_call.function.arguments = '{"task_id": "test-task-id"}'
        mock_tool_call.id = "test_call_id"
        mock_response.choices[0].message.tool_calls = [mock_tool_call]
        
        mock_final_response = AsyncMock()
        mock_final_response.choices = [AsyncMock()]
        mock_final_response.choices[0].message = AsyncMock()
        mock_final_response.choices[0].message.content = "I've successfully deleted the task."
        
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool call
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Delete the task with ID test-task-id",
            conversation_id=conversation.id
        )
        
        # Verify that the success confirmation is properly formatted
        assert "successfully" in result["response"].lower()
        assert "deleted" in result["response"].lower()
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_success_confirmation_formatting_for_list_tasks():
    """
    Test that success confirmations for task listing are properly formatted
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_list_confirm"
    conversation = conversation_service.create_conversation(user_id, "List Confirmation Test")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.list_tasks') as mock_list_tasks:
        
        # Mock successful task listing
        mock_list_tasks.return_value = {
            "success": True,
            "tasks": [
                {"task_id": "task1", "title": "First task", "status": "pending"},
                {"task_id": "task2", "title": "Second task", "status": "completed"}
            ],
            "user_id": user_id,
            "count": 2
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
        mock_final_response.choices[0].message.content = "I found 2 tasks: First task, Second task."
        
        mock_openai.chat.completions.create.side_effect = [mock_response, mock_final_response]
        
        # Create agent runner and run with a message that triggers tool call
        agent_runner = AgentRunner(db_session)
        
        result = await agent_runner.run_agent(
            user_id=user_id,
            message="Show me my tasks",
            conversation_id=conversation.id
        )
        
        # Verify that the success confirmation is properly formatted
        assert "found" in result["response"].lower()
        assert "2 tasks" in result["response"]
        assert "First task" in result["response"]
        assert "Second task" in result["response"]
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()