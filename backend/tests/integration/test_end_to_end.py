"""
End-to-end tests covering all user stories
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4

from src.models.conversation import Conversation, Message
from src.services.conversation_service import ConversationService
from src.database.connection import get_db_session
from src.services.agent_runner import AgentRunner


@pytest.mark.asyncio
async def test_end_to_end_user_story_1_natural_language_task_management():
    """
    End-to-end test for User Story 1: Natural Language Task Management
    As a user, I want to manage my tasks using natural language through the chat interface
    so that I can express my intentions in plain English without needing to learn specific commands.
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_e2e_us1"
    conversation = conversation_service.create_conversation(user_id, "E2E Test US1")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.create_task') as mock_create_task, \
         patch('src.services.mcp_integration.MCPTaskService.list_tasks') as mock_list_tasks:
        
        # Mock successful task creation
        mock_create_task.return_value = {
            "success": True,
            "task_id": "test-task-id-1",
            "title": "buy groceries",
            "description": "Get milk, bread, and eggs",
            "user_id": user_id,
            "status": "pending"
        }
        
        # Mock successful task listing
        mock_list_tasks.return_value = {
            "success": True,
            "tasks": [
                {"task_id": "test-task-id-1", "title": "buy groceries", "status": "pending"}
            ],
            "user_id": user_id,
            "count": 1
        }
        
        # Mock the OpenAI response to first create a task
        mock_response_create = AsyncMock()
        mock_response_create.choices = [AsyncMock()]
        mock_response_create.choices[0].message = AsyncMock()
        mock_response_create.choices[0].message.content = None
        
        # Mock a tool call to create_task
        mock_tool_call_create = MagicMock()
        mock_tool_call_create.function.name = "create_task"
        mock_tool_call_create.function.arguments = '{"title": "buy groceries", "description": "Get milk, bread, and eggs"}'
        mock_tool_call_create.id = "create_call_id"
        mock_response_create.choices[0].message.tool_calls = [mock_tool_call_create]
        
        # Mock the final response after tool execution
        mock_final_response_create = AsyncMock()
        mock_final_response_create.choices = [AsyncMock()]
        mock_final_response_create.choices[0].message = AsyncMock()
        mock_final_response_create.choices[0].message.content = "I've successfully created the task 'buy groceries'."
        
        # First sequence: create task
        mock_openai.chat.completions.create.side_effect = [mock_response_create, mock_final_response_create]
        
        # Create agent runner and run the first command
        agent_runner = AgentRunner(db_session)
        
        result1 = await agent_runner.run_agent(
            user_id=user_id,
            message="Add a task to buy groceries",
            conversation_id=conversation.id
        )
        
        # Verify the task creation response
        assert "buy groceries" in result1["response"]
        assert "successfully created" in result1["response"].lower()
        
        # Now test the second command to list tasks
        mock_response_list = AsyncMock()
        mock_response_list.choices = [AsyncMock()]
        mock_response_list.choices[0].message = AsyncMock()
        mock_response_list.choices[0].message.content = None
        
        # Mock a tool call to list_tasks
        mock_tool_call_list = MagicMock()
        mock_tool_call_list.function.name = "list_tasks"
        mock_tool_call_list.function.arguments = f'{{"user_id": "{user_id}"}}'
        mock_tool_call_list.id = "list_call_id"
        mock_response_list.choices[0].message.tool_calls = [mock_tool_call_list]
        
        # Mock the final response after tool execution
        mock_final_response_list = AsyncMock()
        mock_final_response_list.choices = [AsyncMock()]
        mock_final_response_list.choices[0].message = AsyncMock()
        mock_final_response_list.choices[0].message.content = "I found 1 task: buy groceries."
        
        # Second sequence: list tasks (side effect continues from previous)
        mock_openai.chat.completions.create.side_effect = [
            mock_response_create, mock_final_response_create,  # First call sequence
            mock_response_list, mock_final_response_list       # Second call sequence
        ]
        
        # Run the second command in the same conversation
        result2 = await agent_runner.run_agent(
            user_id=user_id,
            message="Show me my tasks",
            conversation_id=conversation.id
        )
        
        # Verify the task listing response
        assert "found 1 task" in result2["response"].lower()
        assert "buy groceries" in result2["response"]
        
        # Verify conversation has both user messages and both assistant responses
        messages = conversation_service.get_messages_by_conversation(conversation.id)
        user_messages = [msg for msg in messages if msg.role == "user"]
        assistant_messages = [msg for msg in messages if msg.role == "assistant"]
        
        assert len(user_messages) == 2
        assert len(assistant_messages) == 2
        
        user_contents = [msg.content for msg in user_messages]
        assert "Add a task to buy groceries" in user_contents
        assert "Show me my tasks" in user_contents
        
        assistant_contents = [msg.content for msg in assistant_messages]
        assert any("buy groceries" in content and "created" in content for content in assistant_contents)
        assert any("found 1 task" in content.lower() for content in assistant_contents)
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_end_to_end_user_story_2_persistent_conversation_context():
    """
    End-to-end test for User Story 2: Persistent Conversation Context
    As a user, I want my conversation with the AI agent to maintain context
    so that I can have a natural, flowing conversation without repeating myself.
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_e2e_us2"
    conversation = conversation_service.create_conversation(user_id, "E2E Test US2")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.create_task') as mock_create_task, \
         patch('src.services.mcp_integration.MCPTaskService.update_task') as mock_update_task:
        
        # Mock successful task creation
        mock_create_task.return_value = {
            "success": True,
            "task_id": "test-task-id-2",
            "title": "grocery shopping",
            "description": "Buy milk and bread",
            "user_id": user_id,
            "status": "pending"
        }
        
        # Mock successful task update
        mock_update_task.return_value = {
            "success": True,
            "task_id": "test-task-id-2",
            "title": "grocery shopping",
            "status": "completed"
        }
        
        # First interaction: Create a task
        mock_response_create = AsyncMock()
        mock_response_create.choices = [AsyncMock()]
        mock_response_create.choices[0].message = AsyncMock()
        mock_response_create.choices[0].message.content = None
        
        mock_tool_call_create = MagicMock()
        mock_tool_call_create.function.name = "create_task"
        mock_tool_call_create.function.arguments = '{"title": "grocery shopping", "description": "Buy milk and bread"}'
        mock_tool_call_create.id = "create_call_id"
        mock_response_create.choices[0].message.tool_calls = [mock_tool_call_create]
        
        mock_final_response_create = AsyncMock()
        mock_final_response_create.choices = [AsyncMock()]
        mock_final_response_create.choices[0].message = AsyncMock()
        mock_final_response_create.choices[0].message.content = "I've successfully created the task 'grocery shopping'."
        
        # Second interaction: Update the task (using context from previous conversation)
        mock_response_update = AsyncMock()
        mock_response_update.choices = [AsyncMock()]
        mock_response_update.choices[0].message = AsyncMock()
        mock_response_update.choices[0].message.content = None
        
        mock_tool_call_update = MagicMock()
        mock_tool_call_update.function.name = "update_task"
        # Note: The AI agent should infer the task_id from the conversation context
        mock_tool_call_update.function.arguments = '{"task_id": "test-task-id-2", "status": "completed"}'
        mock_tool_call_update.id = "update_call_id"
        mock_response_update.choices[0].message.tool_calls = [mock_tool_call_update]
        
        mock_final_response_update = AsyncMock()
        mock_final_response_update.choices = [AsyncMock()]
        mock_final_response_update.choices[0].message = AsyncMock()
        mock_final_response_update.choices[0].message.content = "I've successfully updated the task 'grocery shopping'."
        
        # Set up the side effect to return different responses for different calls
        call_count = 0
        def mock_side_effect(*args, **kwargs):
            nonlocal call_count
            if call_count == 0 or call_count == 1:
                # First call sequence (create task)
                call_count += 1
                if call_count == 1:
                    return mock_response_create
                else:
                    # Reset for next call
                    call_count = 2
                    return mock_final_response_create
            elif call_count == 2 or call_count == 3:
                # Second call sequence (update task)
                call_count += 1
                if call_count == 3:
                    return mock_response_update
                else:
                    # Reset for next sequence
                    call_count = 4
                    return mock_final_response_update
            else:
                # Default response
                return mock_final_response_update
        
        mock_openai.chat.completions.create.side_effect = lambda *args, **kwargs: mock_side_effect()
        
        # Create agent runner and run the first command
        agent_runner = AgentRunner(db_session)
        
        result1 = await agent_runner.run_agent(
            user_id=user_id,
            message="Create a task to go grocery shopping for milk and bread",
            conversation_id=conversation.id
        )
        
        # Verify the task creation response
        assert "grocery shopping" in result1["response"]
        assert "successfully created" in result1["response"].lower()
        
        # Run the second command in the same conversation (context should be preserved)
        result2 = await agent_runner.run_agent(
            user_id=user_id,
            message="Mark the grocery shopping task as completed",
            conversation_id=conversation.id
        )
        
        # Verify the task update response
        assert "grocery shopping" in result2["response"]
        assert "successfully updated" in result2["response"].lower()
        
        # Verify conversation context was maintained
        messages = conversation_service.get_messages_by_conversation(conversation.id)
        user_messages = [msg for msg in messages if msg.role == "user"]
        assistant_messages = [msg for msg in messages if msg.role == "assistant"]
        
        assert len(user_messages) == 2
        assert len(assistant_messages) == 2
        
        # The second user message referred to "the grocery shopping task" without repeating full details
        # This verifies that context was maintained between interactions
        user_contents = [msg.content for msg in user_messages]
        assert "Create a task to go grocery shopping for milk and bread" in user_contents[0]
        assert "Mark the grocery shopping task as completed" in user_contents[1]
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()


@pytest.mark.asyncio
async def test_end_to_end_user_story_3_reliable_task_operations():
    """
    End-to-end test for User Story 3: Reliable Task Operations
    As a user, I want to be confident that my task management operations are reliable
    and that I receive clear feedback about the results so that I can trust the system
    to correctly handle my tasks.
    """
    db_session = next(get_db_session())
    conversation_service = ConversationService(db_session)
    
    # Create a conversation
    user_id = "test_user_e2e_us3"
    conversation = conversation_service.create_conversation(user_id, "E2E Test US3")
    
    with patch('src.services.agent_runner.client') as mock_openai, \
         patch('src.services.mcp_integration.MCPTaskService.create_task') as mock_create_task, \
         patch('src.services.mcp_integration.MCPTaskService.list_tasks') as mock_list_tasks:
        
        # First, mock a successful task creation
        mock_create_task.return_value = {
            "success": True,
            "task_id": "test-task-id-3",
            "title": "schedule meeting",
            "description": "Schedule team sync for Friday",
            "user_id": user_id,
            "status": "pending"
        }
        
        # Then, mock successful task listing
        mock_list_tasks.return_value = {
            "success": True,
            "tasks": [
                {"task_id": "test-task-id-3", "title": "schedule meeting", "status": "pending"}
            ],
            "user_id": user_id,
            "count": 1
        }
        
        # First interaction: Create a task
        mock_response_create = AsyncMock()
        mock_response_create.choices = [AsyncMock()]
        mock_response_create.choices[0].message = AsyncMock()
        mock_response_create.choices[0].message.content = None
        
        mock_tool_call_create = MagicMock()
        mock_tool_call_create.function.name = "create_task"
        mock_tool_call_create.function.arguments = '{"title": "schedule meeting", "description": "Schedule team sync for Friday"}'
        mock_tool_call_create.id = "create_call_id"
        mock_response_create.choices[0].message.tool_calls = [mock_tool_call_create]
        
        mock_final_response_create = AsyncMock()
        mock_final_response_create.choices = [AsyncMock()]
        mock_final_response_create.choices[0].message = AsyncMock()
        mock_final_response_create.choices[0].message.content = "I've successfully created the task 'schedule meeting'."
        
        # Second interaction: List tasks to verify creation
        mock_response_list = AsyncMock()
        mock_response_list.choices = [AsyncMock()]
        mock_response_list.choices[0].message = AsyncMock()
        mock_response_list.choices[0].message.content = None
        
        mock_tool_call_list = MagicMock()
        mock_tool_call_list.function.name = "list_tasks"
        mock_tool_call_list.function.arguments = f'{{"user_id": "{user_id}"}}'
        mock_tool_call_list.id = "list_call_id"
        mock_response_list.choices[0].message.tool_calls = [mock_tool_call_list]
        
        mock_final_response_list = AsyncMock()
        mock_final_response_list.choices = [AsyncMock()]
        mock_final_response_list.choices[0].message = AsyncMock()
        mock_final_response_list.choices[0].message.content = "I found 1 task: schedule meeting."
        
        # Set up the side effect for both sequences
        call_count = 0
        def mock_side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                # First sequence (create task)
                return mock_response_create if call_count == 1 else mock_final_response_create
            else:
                # Second sequence (list tasks)
                return mock_response_list if call_count == 3 else mock_final_response_list
        
        mock_openai.chat.completions.create.side_effect = mock_side_effect
        
        # Create agent runner and run the first command
        agent_runner = AgentRunner(db_session)
        
        result1 = await agent_runner.run_agent(
            user_id=user_id,
            message="Create a task to schedule a team sync meeting for Friday",
            conversation_id=conversation.id
        )
        
        # Verify the successful task creation response
        assert "schedule meeting" in result1["response"]
        assert "successfully created" in result1["response"].lower()
        
        # Run the second command to verify the task was indeed created
        result2 = await agent_runner.run_agent(
            user_id=user_id,
            message="Show me my tasks",
            conversation_id=conversation.id
        )
        
        # Verify the task listing response confirms the task exists
        assert "found 1 task" in result2["response"].lower()
        assert "schedule meeting" in result2["response"]
        
        # Verify that both successful operations had clear feedback
        messages = conversation_service.get_messages_by_conversation(conversation.id)
        assistant_messages = [msg for msg in messages if msg.role == "assistant"]
        
        # Both assistant responses should contain clear feedback about the operations
        success_feedback_count = 0
        for msg in assistant_messages:
            if "successfully" in msg.content.lower() or "found" in msg.content.lower():
                success_feedback_count += 1
        
        assert success_feedback_count >= 2, "Both operations should have provided clear success feedback"
        
        # Clean up
        db_session.delete(conversation)
        db_session.commit()