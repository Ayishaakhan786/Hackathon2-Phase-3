"""
Input sanitization and security validation
"""
import re
from typing import Dict, Any, Optional
from html import escape
import bleach


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS and other injection attacks
    
    Args:
        text: The input text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return text
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Escape HTML characters
    text = escape(text, quote=True)
    
    # Remove potentially dangerous patterns
    # Remove javascript:, vbscript:, data: URIs
    dangerous_patterns = [
        r'(?i)javascript:',
        r'(?i)vbscript:',
        r'(?i)data:',
        r'(?i)on\w+\s*=',
    ]
    
    for pattern in dangerous_patterns:
        text = re.sub(pattern, '', text)
    
    return text


def validate_user_message(message: str) -> Dict[str, Any]:
    """
    Validate and sanitize a user message
    
    Args:
        message: The user message to validate
        
    Returns:
        Dictionary with validation results
    """
    result = {
        "is_valid": True,
        "sanitized_message": message,
        "errors": [],
        "warnings": []
    }
    
    # Check if message is empty
    if not message or not message.strip():
        result["is_valid"] = False
        result["errors"].append("Message cannot be empty")
        return result
    
    # Check message length
    if len(message) > 10000:  # 10KB limit
        result["is_valid"] = False
        result["errors"].append("Message exceeds maximum length of 10,000 characters")
        return result
    
    # Sanitize the message
    sanitized = sanitize_input(message)
    result["sanitized_message"] = sanitized
    
    # Check for potential prompt injection attempts
    prompt_injection_patterns = [
        r"(?i)\b(ignore|disregard|forget)\b.*\binstructions?\b",
        r"(?i)\b(?:system|user|assistant)\b.*:",
        r"(?i)^\s*---\s*$",  # Markdown separators
        r"(?i)^\s*\[\[[^\]]*\]\]\s*$",  # Wiki-style links that might be used maliciously
    ]
    
    for pattern in prompt_injection_patterns:
        if re.search(pattern, message):
            result["warnings"].append("Potential prompt injection attempt detected")
    
    return result


def validate_user_id(user_id: str) -> Dict[str, Any]:
    """
    Validate a user ID
    
    Args:
        user_id: The user ID to validate
        
    Returns:
        Dictionary with validation results
    """
    result = {
        "is_valid": True,
        "sanitized_user_id": user_id,
        "errors": []
    }
    
    if not user_id:
        result["is_valid"] = False
        result["errors"].append("User ID cannot be empty")
        return result
    
    # Check length
    if len(user_id) > 255:
        result["is_valid"] = False
        result["errors"].append("User ID exceeds maximum length of 255 characters")
        return result
    
    # Only allow alphanumeric, hyphens, underscores, and periods
    if not re.match(r'^[a-zA-Z0-9._-]+$', user_id):
        result["is_valid"] = False
        result["errors"].append("User ID contains invalid characters. Only alphanumeric, hyphens, underscores, and periods are allowed.")
        return result
    
    return result


def validate_conversation_id(conversation_id: str) -> Dict[str, Any]:
    """
    Validate a conversation ID
    
    Args:
        conversation_id: The conversation ID to validate
        
    Returns:
        Dictionary with validation results
    """
    result = {
        "is_valid": True,
        "errors": []
    }
    
    if not conversation_id:
        # Empty conversation ID is valid (means create new conversation)
        return result
    
    # Check if it's a valid UUID format
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, conversation_id, re.IGNORECASE):
        result["is_valid"] = False
        result["errors"].append("Invalid conversation ID format. Must be a valid UUID.")
    
    return result


def sanitize_metadata(metadata: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Sanitize metadata dictionary
    
    Args:
        metadata: The metadata to sanitize
        
    Returns:
        Sanitized metadata
    """
    if not metadata:
        return metadata
    
    sanitized = {}
    for key, value in metadata.items():
        # Sanitize keys
        if not isinstance(key, str):
            continue  # Skip non-string keys
        
        # Limit key length
        if len(key) > 100:
            continue  # Skip overly long keys
        
        # Only allow alphanumeric, hyphens, underscores in keys
        if not re.match(r'^[a-zA-Z0-9_-]+$', key):
            continue  # Skip invalid keys
        
        # Sanitize values based on type
        if isinstance(value, str):
            sanitized[key] = sanitize_input(value)
        elif isinstance(value, (int, float, bool)):
            sanitized[key] = value
        elif isinstance(value, dict):
            sanitized[key] = sanitize_metadata(value)
        elif isinstance(value, list):
            # Sanitize list items
            sanitized_list = []
            for item in value:
                if isinstance(item, str):
                    sanitized_list.append(sanitize_input(item))
                elif isinstance(item, dict):
                    sanitized_list.append(sanitize_metadata(item))
                else:
                    sanitized_list.append(item)
            sanitized[key] = sanitized_list
        else:
            # For other types, just include them as-is
            sanitized[key] = value
    
    return sanitized


def validate_chat_request(message: str, user_id: str, conversation_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Validate a chat request with all its components
    
    Args:
        message: The user message
        user_id: The user ID
        conversation_id: The optional conversation ID
        metadata: The optional metadata
        
    Returns:
        Dictionary with validation results
    """
    result = {
        "is_valid": True,
        "sanitized_message": message,
        "sanitized_user_id": user_id,
        "sanitized_conversation_id": conversation_id,
        "sanitized_metadata": metadata,
        "errors": [],
        "warnings": []
    }
    
    # Validate message
    message_validation = validate_user_message(message)
    if not message_validation["is_valid"]:
        result["is_valid"] = False
        result["errors"].extend(message_validation["errors"])
    else:
        result["sanitized_message"] = message_validation["sanitized_message"]
        result["warnings"].extend(message_validation["warnings"])
    
    # Validate user ID
    user_validation = validate_user_id(user_id)
    if not user_validation["is_valid"]:
        result["is_valid"] = False
        result["errors"].extend(user_validation["errors"])
    else:
        result["sanitized_user_id"] = user_validation["sanitized_user_id"]
    
    # Validate conversation ID
    conv_validation = validate_conversation_id(conversation_id)
    if not conv_validation["is_valid"]:
        result["is_valid"] = False
        result["errors"].extend(conv_validation["errors"])
    else:
        result["sanitized_conversation_id"] = conversation_id
    
    # Sanitize metadata
    result["sanitized_metadata"] = sanitize_metadata(metadata)
    
    return result