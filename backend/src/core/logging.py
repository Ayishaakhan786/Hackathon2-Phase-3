"""
Comprehensive logging for agent operations and tool calls
"""
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID


# Configure logger for agent operations
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a handler for agent-specific logs
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter for agent logs
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - AGENT_ID:%(agent_id)s - CONV_ID:%(conversation_id)s - %(message)s'
)
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)
logger.propagate = False  # Prevent duplicate logs


def log_agent_operation(
    operation_type: str,
    conversation_id: str,
    user_id: str,
    agent_id: Optional[str] = None,
    input_message: Optional[str] = None,
    output_message: Optional[str] = None,
    duration_ms: Optional[float] = None,
    success: bool = True,
    error_details: Optional[Dict[str, Any]] = None
):
    """
    Log an agent operation with comprehensive details
    
    Args:
        operation_type: Type of operation (e.g., 'chat_process', 'tool_call', 'context_build')
        conversation_id: ID of the conversation
        user_id: ID of the user
        agent_id: ID of the agent (optional)
        input_message: Input message to the agent
        output_message: Output message from the agent
        duration_ms: Duration of the operation in milliseconds
        success: Whether the operation was successful
        error_details: Details about any errors that occurred
    """
    extra = {
        'agent_id': agent_id or 'default',
        'conversation_id': conversation_id,
        'user_id': user_id
    }
    
    log_data = {
        'operation_type': operation_type,
        'conversation_id': conversation_id,
        'user_id': user_id,
        'timestamp': datetime.utcnow().isoformat(),
        'success': success
    }
    
    if input_message:
        log_data['input_message'] = input_message
    if output_message:
        log_data['output_message'] = output_message
    if duration_ms:
        log_data['duration_ms'] = duration_ms
    if error_details:
        log_data['error_details'] = error_details
    
    if success:
        logger.info(json.dumps(log_data), extra=extra)
    else:
        logger.error(json.dumps(log_data), extra=extra)


def log_tool_call(
    tool_name: str,
    conversation_id: str,
    user_id: str,
    agent_id: Optional[str] = None,
    input_params: Optional[Dict[str, Any]] = None,
    output_result: Optional[Dict[str, Any]] = None,
    duration_ms: Optional[float] = None,
    success: bool = True,
    error_details: Optional[Dict[str, Any]] = None
):
    """
    Log a tool call with comprehensive details
    
    Args:
        tool_name: Name of the tool being called
        conversation_id: ID of the conversation
        user_id: ID of the user
        agent_id: ID of the agent (optional)
        input_params: Parameters passed to the tool
        output_result: Result returned by the tool
        duration_ms: Duration of the tool call in milliseconds
        success: Whether the tool call was successful
        error_details: Details about any errors that occurred
    """
    extra = {
        'agent_id': agent_id or 'default',
        'conversation_id': conversation_id,
        'user_id': user_id
    }
    
    log_data = {
        'operation_type': 'tool_call',
        'tool_name': tool_name,
        'conversation_id': conversation_id,
        'user_id': user_id,
        'timestamp': datetime.utcnow().isoformat(),
        'success': success
    }
    
    if input_params:
        log_data['input_params'] = input_params
    if output_result:
        log_data['output_result'] = output_result
    if duration_ms:
        log_data['duration_ms'] = duration_ms
    if error_details:
        log_data['error_details'] = error_details
    
    if success:
        logger.info(json.dumps(log_data), extra=extra)
    else:
        logger.error(json.dumps(log_data), extra=extra)


def log_conversation_event(
    event_type: str,
    conversation_id: str,
    user_id: str,
    agent_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
):
    """
    Log a conversation event
    
    Args:
        event_type: Type of event (e.g., 'conversation_start', 'message_added', 'context_retrieved')
        conversation_id: ID of the conversation
        user_id: ID of the user
        agent_id: ID of the agent (optional)
        details: Additional details about the event
    """
    extra = {
        'agent_id': agent_id or 'default',
        'conversation_id': conversation_id,
        'user_id': user_id
    }
    
    log_data = {
        'event_type': event_type,
        'conversation_id': conversation_id,
        'user_id': user_id,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if details:
        log_data['details'] = details
    
    logger.info(json.dumps(log_data), extra=extra)