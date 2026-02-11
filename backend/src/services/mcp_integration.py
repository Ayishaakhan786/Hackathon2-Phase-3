import json
from typing import Dict, Any, Optional
from sqlmodel import Session, select
from uuid import UUID
import uuid
from ..config.settings import settings
from ..models.task import Task
from ..services.error_responses import create_error_response, format_tool_error_response, ErrorCode


class MCPTaskService:
    """
    MCP integration service that connects to actual task operations in the database.
    This implementation persists data in Neon DB as required by the specification.
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    async def create_task(self, title: str, description: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new task in the database
        """
        try:
            # Create a new task instance
            task = Task(
                id=uuid.uuid4(),
                title=title,
                description=description,
                user_id=user_id,
                status="pending"
            )
            
            # Add to database
            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)
            
            result = {
                "success": True,
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "user_id": task.user_id,
                "status": task.status
            }
            
            print(f"MCP Tool Called: create_task - {result}")
            return result
        except Exception as e:
            self.db_session.rollback()
            result = create_error_response(
                error_code=ErrorCode.DATABASE_ERROR,
                message=f"Failed to create task: {str(e)}",
                details={"original_error": str(e)},
                user_friendly_message="I couldn't create the task. Please try again or check your input."
            )
            print(f"MCP Tool Error: create_task - {result}")
            return result
    
    async def update_task(self, task_id: str, title: Optional[str] = None, 
                         description: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing task in the database
        """
        try:
            # Get the task from database
            task_uuid = UUID(task_id)
            task = self.db_session.get(Task, task_uuid)
            
            if not task:
                result = create_error_response(
                    error_code=ErrorCode.RESOURCE_NOT_FOUND,
                    message=f"No task found with id {task_id}",
                    details={"task_id": task_id},
                    user_friendly_message="I couldn't find the task you're looking for. Please check the task ID."
                )
                print(f"MCP Tool Error: update_task - {result}")
                return result
            
            # Update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if status is not None:
                task.status = status
            
            # Commit changes
            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)
            
            result = {
                "success": True,
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": task.status
            }
            
            print(f"MCP Tool Called: update_task - {result}")
            return result
        except Exception as e:
            self.db_session.rollback()
            result = create_error_response(
                error_code=ErrorCode.DATABASE_ERROR,
                message=f"Failed to update task: {str(e)}",
                details={"original_error": str(e), "task_id": task_id},
                user_friendly_message="I couldn't update the task. Please try again or check your input."
            )
            print(f"MCP Tool Error: update_task - {result}")
            return result
    
    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        Delete a task from the database
        """
        try:
            # Get the task from database
            task_uuid = UUID(task_id)
            task = self.db_session.get(Task, task_uuid)
            
            if not task:
                result = create_error_response(
                    error_code=ErrorCode.RESOURCE_NOT_FOUND,
                    message=f"No task found with id {task_id}",
                    details={"task_id": task_id},
                    user_friendly_message="I couldn't find the task you're looking for. Please check the task ID."
                )
                print(f"MCP Tool Error: delete_task - {result}")
                return result
            
            # Delete the task
            self.db_session.delete(task)
            self.db_session.commit()
            
            result = {
                "success": True,
                "task_id": task_id
            }
            
            print(f"MCP Tool Called: delete_task - {result}")
            return result
        except Exception as e:
            self.db_session.rollback()
            result = create_error_response(
                error_code=ErrorCode.DATABASE_ERROR,
                message=f"Failed to delete task: {str(e)}",
                details={"original_error": str(e), "task_id": task_id},
                user_friendly_message="I couldn't delete the task. Please try again."
            )
            print(f"MCP Tool Error: delete_task - {result}")
            return result
    
    async def list_tasks(self, user_id: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """
        List tasks from the database with optional filters
        """
        try:
            # Build query with optional filters
            query = select(Task)
            if user_id:
                query = query.where(Task.user_id == user_id)
            if status:
                query = query.where(Task.status == status)
            
            # Execute query
            results = self.db_session.exec(query)
            tasks = results.all()
            
            # Format results
            task_list = []
            for task in tasks:
                task_list.append({
                    "task_id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "user_id": task.user_id
                })
            
            result = {
                "success": True,
                "tasks": task_list,
                "user_id": user_id,
                "status_filter": status,
                "count": len(task_list)
            }
            
            print(f"MCP Tool Called: list_tasks - {len(task_list)} tasks returned")
            return result
        except Exception as e:
            result = create_error_response(
                error_code=ErrorCode.DATABASE_ERROR,
                message=f"Failed to list tasks: {str(e)}",
                details={"original_error": str(e), "user_id": user_id, "status": status},
                user_friendly_message="I couldn't retrieve your tasks. Please try again."
            )
            print(f"MCP Tool Error: list_tasks - {result}")
            return result


# Note: The service instance will be created with a session when needed
def get_mcp_service(db_session: Session):
    """
    Factory function to create an MCP service instance with a database session
    """
    return MCPTaskService(db_session)