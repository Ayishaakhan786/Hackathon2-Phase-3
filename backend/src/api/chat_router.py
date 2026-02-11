from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from uuid import UUID
from typing import Optional
from ..models.chat import ChatRequest, ChatResponse
from ..api.deps import get_db_session, validate_user_id
from ..services.agent_runner import AgentRunner
from ..middleware.rate_limit import check_rate_limit, get_remaining_limits
from ..core.input_sanitization import validate_chat_request


chat_router = APIRouter()


@chat_router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: Request,  # Add request parameter to access client IP
    user_id: str,
    chat_request: ChatRequest,
    db_session: Session = Depends(get_db_session)
):
    """
    Main endpoint for chatting with the AI agent
    """
    # Validate user ID format
    validated_user_id = validate_user_id(user_id)

    # Get client IP address for rate limiting
    client_ip = request.client.host if request.client else "127.0.0.1"

    # Check rate limits
    rate_status = check_rate_limit(validated_user_id, client_ip)
    
    if not rate_status["user_allowed"]:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded: Too many requests for this user"
        )
    
    if not rate_status["ip_allowed"]:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded: Too many requests from this IP address"
        )

    # Validate and sanitize the entire chat request
    validation_result = validate_chat_request(
        message=chat_request.message,
        user_id=validated_user_id,
        conversation_id=chat_request.conversation_id,
        metadata=chat_request.metadata
    )
    
    if not validation_result["is_valid"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request: {'; '.join(validation_result['errors'])}"
        )

    # Use sanitized values
    sanitized_message = validation_result["sanitized_message"]
    sanitized_conversation_id = validation_result["sanitized_conversation_id"]
    sanitized_metadata = validation_result["sanitized_metadata"]

    # Validate conversation ID if provided
    conversation_id = None
    if sanitized_conversation_id:
        try:
            conversation_id = UUID(sanitized_conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid conversation ID format: {sanitized_conversation_id}"
            )

    # Initialize the agent runner
    agent_runner = AgentRunner(db_session)

    try:
        # Run the agent with the sanitized message
        result = await agent_runner.run_agent(
            user_id=validated_user_id,
            message=sanitized_message,
            conversation_id=conversation_id
        )

        # Format the response
        response = ChatResponse(
            conversation_id=result["conversation_id"],
            message={"role": "assistant", "content": result["response"]},
            timestamp="2026-02-11T02:11:00Z",  # In a real implementation, use actual timestamp
            next_action="continue"
        )

        return response
    except ValueError as e:
        # Handle value errors (e.g., invalid conversation ID)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle any other errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")