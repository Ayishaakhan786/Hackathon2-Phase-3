"""
Standardized error response format for agent
"""
from typing import Dict, Any, Optional
from enum import Enum


class ErrorCode(Enum):
    """Enumeration of possible error codes"""
    INVALID_INPUT = "INVALID_INPUT"
    TOOL_EXECUTION_FAILED = "TOOL_EXECUTION_FAILED"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


def create_error_response(
    error_code: ErrorCode,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    user_friendly_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a standardized error response
    
    Args:
        error_code: The error code from ErrorCode enum
        message: Technical error message
        details: Additional error details
        user_friendly_message: Optional user-friendly message to display to end users
    
    Returns:
        Dictionary containing standardized error response
    """
    error_response = {
        "success": False,
        "error_code": error_code.value,
        "message": message,
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }
    
    if details:
        error_response["details"] = details
    
    if user_friendly_message:
        error_response["user_message"] = user_friendly_message
    else:
        # Default user-friendly message based on error code
        default_user_messages = {
            ErrorCode.INVALID_INPUT: "The input provided is invalid. Please check your request and try again.",
            ErrorCode.TOOL_EXECUTION_FAILED: "The requested operation failed to execute. Please try again.",
            ErrorCode.DATABASE_ERROR: "A database error occurred. Please try again later.",
            ErrorCode.EXTERNAL_SERVICE_ERROR: "An external service is temporarily unavailable. Please try again later.",
            ErrorCode.AUTHENTICATION_FAILED: "Authentication failed. Please check your credentials.",
            ErrorCode.UNAUTHORIZED_ACCESS: "You are not authorized to perform this action.",
            ErrorCode.RESOURCE_NOT_FOUND: "The requested resource was not found.",
            ErrorCode.RATE_LIMIT_EXCEEDED: "You have exceeded the rate limit. Please try again later.",
            ErrorCode.INTERNAL_ERROR: "An internal error occurred. Please try again later."
        }
        error_response["user_message"] = default_user_messages.get(error_code, "An error occurred. Please try again.")
    
    return error_response


def create_success_response(data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standardized success response
    
    Args:
        data: Optional data to include in the response
    
    Returns:
        Dictionary containing standardized success response
    """
    response = {
        "success": True,
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }
    
    if data:
        response.update(data)
    
    return response


def format_tool_error_response(original_error: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format an error from a tool call into a standardized response
    
    Args:
        original_error: The original error response from a tool
    
    Returns:
        Standardized error response
    """
    # Determine the appropriate error code based on the original error
    error_code = ErrorCode.TOOL_EXECUTION_FAILED
    
    if "database" in str(original_error.get("error", "")).lower():
        error_code = ErrorCode.DATABASE_ERROR
    elif "authentication" in str(original_error.get("error", "")).lower():
        error_code = ErrorCode.AUTHENTICATION_FAILED
    elif "not found" in str(original_error.get("error", "")).lower():
        error_code = ErrorCode.RESOURCE_NOT_FOUND
    
    return create_error_response(
        error_code=error_code,
        message=original_error.get("message", str(original_error)),
        details=original_error,
        user_friendly_message=original_error.get("message", "The requested operation failed.")
    )