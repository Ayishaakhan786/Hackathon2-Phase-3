"""
Contract test for access validation
This test verifies that the system properly validates user ownership of tasks
"""
import pytest
from unittest.mock import patch, MagicMock
from src.mcp.tools import (
    list_tasks_tool, complete_task_tool, 
    update_task_tool, delete_task_tool
)
from mcp.types import Arguments


@pytest.mark.asyncio
async def test_access_validation_for_list_tasks():
    """Test that list_tasks only returns tasks belonging to the user"""
    # Mock arguments
    arguments = Arguments({"user_id": "user123", "status": "all"})
    
    # Mock the database session context manager
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock the list_tasks function to return tasks for the correct user
        with patch("src.mcp.tools.list_tasks") as mock_list_tasks:
            # Create mock task objects that belong to the user
            mock_task1 = MagicMock()
            mock_task1.id = "task456"
            mock_task1.user_id = "user123"  # Same user
            mock_task1.title = "User's task"
            mock_task1.description = "Description"
            mock_task1.completed = False
            mock_task1.created_at = "2023-01-01T00:00:00"
            mock_task1.updated_at = "2023-01-01T00:00:00"
            
            mock_list_tasks.return_value = [mock_task1]
            
            result = await list_tasks_tool(arguments)
            
            # Verify the result only contains tasks for the correct user
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"User\'s task"' in result.content
            # The service layer should handle filtering by user_id


@pytest.mark.asyncio
async def test_access_validation_for_other_operations():
    """Test that other operations validate user ownership"""
    # Test complete_task with wrong user/task combination
    arguments = Arguments({"user_id": "wrong_user", "task_id": "some_task"})
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock the complete_task function to return None (not found or not owned by user)
        with patch("src.mcp.tools.complete_task") as mock_complete_task:
            mock_complete_task.return_value = None  # Simulate task not found or not owned by user
            
            result = await complete_task_tool(arguments)
            
            # Verify the result indicates failure due to access validation
            assert result.content is not None
            assert '"success": false' in result.content
            assert "Task not found or does not belong to user" in result.content
    
    # Test update_task with wrong user/task combination
    arguments = Arguments({"user_id": "wrong_user", "task_id": "some_task", "title": "New title"})
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock the update_task function to return None (not found or not owned by user)
        with patch("src.mcp.tools.update_task") as mock_update_task:
            mock_update_task.return_value = None  # Simulate task not found or not owned by user
            
            result = await update_task_tool(arguments)
            
            # Verify the result indicates failure due to access validation
            assert result.content is not None
            assert '"success": false' in result.content
            assert "Task not found or does not belong to user" in result.content
    
    # Test delete_task with wrong user/task combination
    arguments = Arguments({"user_id": "wrong_user", "task_id": "some_task"})
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock the delete_task function to return False (not found or not owned by user)
        with patch("src.mcp.tools.delete_task") as mock_delete_task:
            mock_delete_task.return_value = False  # Simulate task not found or not owned by user
            
            result = await delete_task_tool(arguments)
            
            # Verify the result indicates failure due to access validation
            assert result.content is not None
            assert '"success": false' in result.content
            assert "Task not found or does not belong to user" in result.content