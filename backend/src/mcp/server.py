import asyncio
from mcp.server import Server
from mcp.types import Tool, Arguments, Result
import json
from typing import Dict, Any

from ..services.task_service import (
    add_task, list_tasks, complete_task, update_task, delete_task
)
from ..db.connection import get_session


class MCPTaskServer:
    """
    MCP Server that exposes task operations as stateless tools.
    All state is persisted in Neon PostgreSQL database.
    """
    
    def __init__(self):
        self.server = Server()
        self._register_tools()
    
    def _register_tools(self):
        """Register all task management tools with the MCP server."""
        # Register add_task tool
        self.server.tools.register(
            name="add_task",
            description="Add a new task for a user",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "title": {"type": "string", "description": "The task title"},
                    "description": {"type": "string", "description": "Optional task description"}
                },
                "required": ["user_id", "title"]
            }
        )(self._handle_add_task)
        
        # Register list_tasks tool
        self.server.tools.register(
            name="list_tasks",
            description="List tasks for a user with optional status filter",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"}
                },
                "required": ["user_id"]
            }
        )(self._handle_list_tasks)
        
        # Register complete_task tool
        self.server.tools.register(
            name="complete_task",
            description="Mark a task as completed",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "string", "description": "The task ID to complete"}
                },
                "required": ["user_id", "task_id"]
            }
        )(self._handle_complete_task)
        
        # Register update_task tool
        self.server.tools.register(
            name="update_task",
            description="Update task details",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "string", "description": "The task ID to update"},
                    "title": {"type": "string", "description": "New title (optional)"},
                    "description": {"type": "string", "description": "New description (optional)"}
                },
                "required": ["user_id", "task_id"]
            }
        )(self._handle_update_task)
        
        # Register delete_task tool
        self.server.tools.register(
            name="delete_task",
            description="Delete a task",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "string", "description": "The task ID to delete"}
                },
                "required": ["user_id", "task_id"]
            }
        )(self._handle_delete_task)
    
    async def _handle_add_task(self, arguments: Arguments) -> Result:
        """Handle the add_task tool call."""
        try:
            user_id = arguments["user_id"]
            title = arguments["title"]
            description = arguments.get("description")
            
            with next(get_session()) as session:
                task = add_task(
                    session=session,
                    user_id=user_id,
                    title=title,
                    description=description
                )
                
                return Result.ok(
                    content=json.dumps({
                        "success": True,
                        "task_id": task.id,
                        "message": "Task added successfully"
                    })
                )
        except Exception as e:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": f"Error adding task: {str(e)}"
                })
            )
    
    async def _handle_list_tasks(self, arguments: Arguments) -> Result:
        """Handle the list_tasks tool call."""
        try:
            user_id = arguments["user_id"]
            status = arguments.get("status", "all")
            
            with next(get_session()) as session:
                from ..services.task_service import TaskStatus
                status_enum = TaskStatus(status)
                
                tasks = list_tasks(
                    session=session,
                    user_id=user_id,
                    status=status_enum
                )
                
                tasks_data = []
                for task in tasks:
                    tasks_data.append({
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat() if task.created_at else None,
                        "updated_at": task.updated_at.isoformat() if task.updated_at else None
                    })
                
                return Result.ok(
                    content=json.dumps({
                        "success": True,
                        "tasks": tasks_data,
                        "message": "Tasks retrieved successfully"
                    })
                )
        except Exception as e:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": f"Error listing tasks: {str(e)}"
                })
            )
    
    async def _handle_complete_task(self, arguments: Arguments) -> Result:
        """Handle the complete_task tool call."""
        try:
            user_id = arguments["user_id"]
            task_id = arguments["task_id"]
            
            with next(get_session()) as session:
                task = complete_task(
                    session=session,
                    user_id=user_id,
                    task_id=task_id
                )
                
                if task:
                    return Result.ok(
                        content=json.dumps({
                            "success": True,
                            "message": "Task marked as completed successfully"
                        })
                    )
                else:
                    return Result.ok(
                        content=json.dumps({
                            "success": False,
                            "message": "Task not found or does not belong to user"
                        })
                    )
        except Exception as e:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": f"Error completing task: {str(e)}"
                })
            )
    
    async def _handle_update_task(self, arguments: Arguments) -> Result:
        """Handle the update_task tool call."""
        try:
            user_id = arguments["user_id"]
            task_id = arguments["task_id"]
            title = arguments.get("title")
            description = arguments.get("description")
            
            from ..models.task import TaskUpdate
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
                
            task_update = TaskUpdate(**update_data)
            
            with next(get_session()) as session:
                task = update_task(
                    session=session,
                    user_id=user_id,
                    task_id=task_id,
                    task_update=task_update
                )
                
                if task:
                    return Result.ok(
                        content=json.dumps({
                            "success": True,
                            "message": "Task updated successfully"
                        })
                    )
                else:
                    return Result.ok(
                        content=json.dumps({
                            "success": False,
                            "message": "Task not found or does not belong to user"
                        })
                    )
        except Exception as e:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": f"Error updating task: {str(e)}"
                })
            )
    
    async def _handle_delete_task(self, arguments: Arguments) -> Result:
        """Handle the delete_task tool call."""
        try:
            user_id = arguments["user_id"]
            task_id = arguments["task_id"]
            
            with next(get_session()) as session:
                success = delete_task(
                    session=session,
                    user_id=user_id,
                    task_id=task_id
                )
                
                if success:
                    return Result.ok(
                        content=json.dumps({
                            "success": True,
                            "message": "Task deleted successfully"
                        })
                    )
                else:
                    return Result.ok(
                        content=json.dumps({
                            "success": False,
                            "message": "Task not found or does not belong to user"
                        })
                    )
        except Exception as e:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": f"Error deleting task: {str(e)}"
                })
            )
    
    def run(self, host: str = "localhost", port: int = 8080):
        """Run the MCP server."""
        print(f"MCP Task Server starting on {host}:{port}")
        self.server.run(host=host, port=port)