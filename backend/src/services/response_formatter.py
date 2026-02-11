"""
Response formatter for ChatKit UI compatibility
"""
from typing import Dict, Any, List
from datetime import datetime


def format_for_chatkit_ui(
    conversation_id: str,
    message_content: str,
    role: str = "assistant",
    timestamp: str = None,
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Format a response to be compatible with ChatKit UI
    
    Args:
        conversation_id: The ID of the conversation
        message_content: The content of the message
        role: The role of the message sender (user, assistant, tool)
        timestamp: ISO 8601 formatted timestamp (will be generated if not provided)
        metadata: Additional metadata to include in the response
    
    Returns:
        Dictionary formatted for ChatKit UI compatibility
    """
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat()
    
    formatted_response = {
        "id": f"msg_{int(datetime.utcnow().timestamp() * 1000000)}",  # Generate a unique message ID
        "conversation_id": conversation_id,
        "senderId": role,
        "text": message_content,
        "createdAt": timestamp,
        "updatedAt": timestamp
    }
    
    if metadata:
        formatted_response["customData"] = metadata
    
    return formatted_response


def format_multiple_messages_for_chatkit(
    conversation_id: str,
    messages: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Format multiple messages for ChatKit UI compatibility
    
    Args:
        conversation_id: The ID of the conversation
        messages: List of messages with 'role' and 'content' keys
    
    Returns:
        List of dictionaries formatted for ChatKit UI compatibility
    """
    formatted_messages = []
    
    for msg in messages:
        role = msg.get('role', 'assistant')
        content = msg.get('content', '')
        timestamp = msg.get('timestamp', datetime.utcnow().isoformat())
        metadata = msg.get('metadata', {})
        
        formatted_msg = format_for_chatkit_ui(
            conversation_id=conversation_id,
            message_content=content,
            role=role,
            timestamp=timestamp,
            metadata=metadata
        )
        
        formatted_messages.append(formatted_msg)
    
    return formatted_messages


def format_success_confirmation(task_operation: str, task_details: Dict[str, Any] = None) -> str:
    """
    Format a success confirmation message
    
    Args:
        task_operation: Description of the task operation that succeeded
        task_details: Optional details about the task
    
    Returns:
        Formatted success confirmation message
    """
    if task_details and 'title' in task_details:
        return f"I've successfully {task_operation} '{task_details['title']}'."
    else:
        return f"I've successfully {task_operation}."


# Response templates for different operation types
RESPONSE_TEMPLATES = {
    "create_success": "I've successfully created the task '{title}'.",
    "create_success_plural": "I've successfully created {count} tasks: {titles}.",
    "create_failure": "I couldn't create the task '{title}'. {error}",
    "update_success": "I've successfully updated the task '{title}'.",
    "update_failure": "I couldn't update the task '{title}'. {error}",
    "delete_success": "I've successfully deleted the task '{title}'.",
    "delete_failure": "I couldn't delete the task '{title}'. {error}",
    "list_success": "I found {count} tasks: {titles}.",
    "list_success_empty": "You don't have any tasks matching those criteria.",
    "list_failure": "I couldn't retrieve your tasks. {error}",
    "generic_success": "Operation completed successfully.",
    "generic_failure": "Operation failed: {error}",
    "confirmation_request": "Would you like me to {action}?",
    "help_response": "I can help you manage your tasks. You can ask me to create, update, delete, or list your tasks.",
    "unknown_command": "I'm not sure how to handle that request. Could you rephrase it?",
    "greeting": "Hello! I'm here to help you manage your tasks. What would you like to do today?"
}


def format_task_operation_success(operation_type: str, task_data: Dict[str, Any]) -> str:
    """
    Format success message for specific task operations
    
    Args:
        operation_type: Type of operation ('create', 'update', 'delete', 'list')
        task_data: Data about the task(s) involved in the operation
    
    Returns:
        Formatted success message
    """
    if operation_type == "create":
        if isinstance(task_data, list) and len(task_data) > 0:
            # Multiple tasks created
            titles = [task.get('title', 'unnamed task') for task in task_data]
            return RESPONSE_TEMPLATES["create_success_plural"].format(
                count=len(titles),
                titles=', '.join(titles)
            )
        else:
            # Single task created
            title = task_data.get('title', 'the task')
            return RESPONSE_TEMPLATES["create_success"].format(title=title)
    
    elif operation_type == "update":
        title = task_data.get('title', 'the task')
        return RESPONSE_TEMPLATES["update_success"].format(title=title)
    
    elif operation_type == "delete":
        title = task_data.get('title', 'the task')
        return RESPONSE_TEMPLATES["delete_success"].format(title=title)
    
    elif operation_type == "list":
        count = task_data.get('count', 0)
        if count == 0:
            return RESPONSE_TEMPLATES["list_success_empty"]
        else:
            titles = [task.get('title', 'unnamed task') for task in task_data.get('tasks', [])]
            if titles:
                return RESPONSE_TEMPLATES["list_success"].format(count=count, titles=', '.join(titles))
            else:
                return f"I found {count} tasks matching your criteria."
    
    else:
        return RESPONSE_TEMPLATES["generic_success"]


def format_task_operation_error(operation_type: str, task_data: Dict[str, Any], error: str = "") -> str:
    """
    Format error message for specific task operations
    
    Args:
        operation_type: Type of operation ('create', 'update', 'delete', 'list')
        task_data: Data about the task(s) involved in the operation
        error: Error message to include in the response
    
    Returns:
        Formatted error message
    """
    if operation_type == "create":
        title = task_data.get('title', 'the task')
        return RESPONSE_TEMPLATES["create_failure"].format(title=title, error=error)
    
    elif operation_type == "update":
        title = task_data.get('title', 'the task')
        return RESPONSE_TEMPLATES["update_failure"].format(title=title, error=error)
    
    elif operation_type == "delete":
        title = task_data.get('title', 'the task')
        return RESPONSE_TEMPLATES["delete_failure"].format(title=title, error=error)
    
    elif operation_type == "list":
        return RESPONSE_TEMPLATES["list_failure"].format(error=error)
    
    else:
        return RESPONSE_TEMPLATES["generic_failure"].format(error=error)


def get_template(template_name: str, **kwargs) -> str:
    """
    Get a formatted response using a named template
    
    Args:
        template_name: Name of the template to use
        **kwargs: Values to substitute into the template
    
    Returns:
        Formatted response string
    """
    if template_name not in RESPONSE_TEMPLATES:
        return f"Template '{template_name}' not found."
    
    template = RESPONSE_TEMPLATES[template_name]
    try:
        return template.format(**kwargs)
    except KeyError as e:
        return f"Missing template parameter: {e}"