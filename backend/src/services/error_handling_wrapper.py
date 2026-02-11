"""
Error handling wrapper for MCP tool calls
"""
import functools
import traceback
from typing import Callable, Any, Dict
from ..services.mcp_integration import MCPTaskService


def handle_mcp_tool_errors(func: Callable) -> Callable:
    """
    Decorator to wrap MCP tool calls with comprehensive error handling
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # Execute the original function
            result = await func(*args, **kwargs)
            
            # If the result already contains error information, return as-is
            if isinstance(result, dict) and result.get("success") is False:
                return result
            
            # Otherwise, return the successful result
            return result
        except Exception as e:
            # Log the error with traceback for debugging
            error_trace = traceback.format_exc()
            print(f"MCP Tool Error in {func.__name__}: {str(e)}")
            print(f"Traceback: {error_trace}")
            
            # Return a standardized error response
            error_result = {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "function": func.__name__,
                "message": "The task operation failed. Please try again or rephrase your request.",
                "details": {
                    "timestamp": __import__('datetime').datetime.utcnow().isoformat()
                }
            }
            
            return error_result
    
    return wrapper


class MCPTaskServiceWithErrorHandling(MCPTaskService):
    """
    MCP Task Service with error handling wrappers applied to all methods
    """
    
    def __init__(self, db_session):
        super().__init__(db_session)
        
        # Apply error handling wrapper to all public methods
        self.create_task = handle_mcp_tool_errors(self.create_task)
        self.update_task = handle_mcp_tool_errors(self.update_task)
        self.delete_task = handle_mcp_tool_errors(self.delete_task)
        self.list_tasks = handle_mcp_tool_errors(self.list_tasks)


def get_mcp_service_with_error_handling(db_session):
    """
    Factory function to create an MCP service instance with error handling
    """
    return MCPTaskServiceWithErrorHandling(db_session)


# Backward compatibility: also provide the original function
def get_mcp_service(db_session):
    """
    Factory function to create an MCP service instance (original version)
    """
    return MCPTaskService(db_session)