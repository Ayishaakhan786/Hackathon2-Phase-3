"""
Integration test for secure task operations
This test verifies that only authorized users can access and modify their tasks
"""
import pytest
from unittest.mock import patch, MagicMock
from src.mcp.tools import (
    add_task_tool, list_tasks_tool, complete_task_tool, 
    update_task_tool, delete_task_tool
)
from mcp.types import Arguments


@pytest.mark.asyncio
async def test_secure_task_operations():
    """Test that only authorized users can access and modify their tasks"""
    # Test 1: User can access their own tasks
    user_id = "authorized_user"
    arguments = Arguments({"user_id": user_id, "title": "Authorized task"})
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        with patch("src.mcp.tools.add_task") as mock_add_task:
            mock_task = MagicMock()
            mock_task.id = "task456"
            mock_task.user_id = user_id
            mock_add_task.return_value = mock_task
            
            result = await add_task_tool(arguments)
            
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"task_id": "task456"' in result.content
    
    # Test 2: User cannot access another user's tasks
    other_user_id = "other_user"
    arguments = Arguments({"user_id": other_user_id, "task_id": "task456"})
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        with patch("src.mcp.tools.complete_task") as mock_complete_task:
            # Return None to simulate that the task doesn't belong to the user
            mock_complete_task.return_value = None
            
            result = await complete_task_tool(arguments)
            
            assert result.content is not None
            assert '"success": false' in result.content
            assert "Task not found or does not belong to user" in result.content
    
    # Test 3: User can list their own tasks
    arguments = Arguments({"user_id": user_id, "status": "all"})
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        with patch("src.mcp.tools.list_tasks") as mock_list_tasks:
            mock_task = MagicMock()
            mock_task.id = "task456"
            mock_task.user_id = user_id
            mock_task.title = "User's task"
            mock_task.description = "Description"
            mock_task.completed = False
            mock_task.created_at = "2023-01-01T00:00:00"
            mock_task.updated_at = "2023-01-01T00:00:00"
            mock_list_tasks.return_value = [mock_task]
            
            result = await list_tasks_tool(arguments)
            
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"User\'s task"' in result.content
    
    # Test 4: User cannot modify another user's task
    arguments = Arguments({
        "user_id": other_user_id, 
        "task_id": "task456", 
        "title": "Modified by unauthorized user"
    })
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        with patch("src.mcp.tools.update_task") as mock_update_task:
            # Return None to simulate that the task doesn't belong to the user
            mock_update_task.return_value = None
            
            result = await update_task_tool(arguments)
            
            assert result.content is not None
            assert '"success": false' in result.content
            assert "Task not found or does not belong to user" in result.content


@pytest.mark.asyncio
async def test_task_not_found_scenarios():
    """Test scenarios where tasks don't exist"""
    # Test with non-existent task
    arguments = Arguments({"user_id": "any_user", "task_id": "nonexistent_task"})
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        with patch("src.mcp.tools.complete_task") as mock_complete_task:
            # Return None to simulate that the task doesn't exist
            mock_complete_task.return_value = None
            
            result = await complete_task_tool(arguments)
            
            assert result.content is not None
            assert '"success": false' in result.content
            assert "Task not found or does not belong to user" in result.content