"""
Integration test for managing tasks
This test verifies that the full flow of managing tasks works correctly
"""
import pytest
from unittest.mock import patch, MagicMock
from src.mcp.tools import (
    list_tasks_tool, complete_task_tool, 
    update_task_tool, delete_task_tool
)
from mcp.types import Arguments
from src.models.task import Task


@pytest.mark.asyncio
async def test_manage_tasks_integration():
    """Test the full flow of managing tasks via the MCP tools"""
    # Test list_tasks
    arguments_list = Arguments({"user_id": "user123", "status": "all"})
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        with patch("src.mcp.tools.list_tasks") as mock_list_tasks:
            # Create mock task objects
            mock_task1 = MagicMock()
            mock_task1.id = "task456"
            mock_task1.user_id = "user123"
            mock_task1.title = "Task 1"
            mock_task1.description = "Description 1"
            mock_task1.completed = False
            mock_task1.created_at = "2023-01-01T00:00:00"
            mock_task1.updated_at = "2023-01-01T00:00:00"
            
            mock_task2 = MagicMock()
            mock_task2.id = "task789"
            mock_task2.user_id = "user123"
            mock_task2.title = "Task 2"
            mock_task2.description = "Description 2"
            mock_task2.completed = True
            mock_task2.created_at = "2023-01-01T00:00:00"
            mock_task2.updated_at = "2023-01-01T00:00:00"
            
            mock_list_tasks.return_value = [mock_task1, mock_task2]
            
            result = await list_tasks_tool(arguments_list)
            
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"tasks"' in result.content
            assert '"Task 1"' in result.content
            assert '"Task 2"' in result.content
    
    # Test complete_task
    arguments_complete = Arguments({"user_id": "user123", "task_id": "task456"})
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        with patch("src.mcp.tools.complete_task") as mock_complete_task:
            mock_task = MagicMock()
            mock_task.id = "task456"
            mock_task.completed = True
            mock_complete_task.return_value = mock_task
            
            result = await complete_task_tool(arguments_complete)
            
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"Task marked as completed successfully"' in result.content
    
    # Test update_task
    arguments_update = Arguments({
        "user_id": "user123", 
        "task_id": "task789", 
        "title": "Updated Task 2", 
        "description": "Updated Description 2"
    })
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        with patch("src.mcp.tools.update_task") as mock_update_task:
            mock_task = MagicMock()
            mock_task.id = "task789"
            mock_task.title = "Updated Task 2"
            mock_task.description = "Updated Description 2"
            mock_update_task.return_value = mock_task
            
            result = await update_task_tool(arguments_update)
            
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"Task updated successfully"' in result.content
    
    # Test delete_task
    arguments_delete = Arguments({"user_id": "user123", "task_id": "task456"})
    
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        with patch("src.mcp.tools.delete_task") as mock_delete_task:
            mock_delete_task.return_value = True
            
            result = await delete_task_tool(arguments_delete)
            
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"Task deleted successfully"' in result.content