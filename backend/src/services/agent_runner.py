import json
from typing import Dict, Any, List
from sqlmodel import Session
from uuid import UUID
from ..services.mcp_integration import get_mcp_service
from ..services.error_handling_wrapper import get_mcp_service_with_error_handling
from ..services.tool_registry import get_tool_registry
from ..config.prompts import TASK_MANAGEMENT_AGENT_PROMPT
from ..config.openai_config import client, OPENAI_MODEL
from ..services.conversation_service import ConversationService
from ..core.logging import log_agent_operation, log_tool_call, log_conversation_event
from ..core.performance_monitor import record_response_time, record_error


class AgentRunner:
    """
    Service class to run the AI agent for task management
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.conversation_service = ConversationService(db_session)
        self.mcp_service = get_mcp_service_with_error_handling(db_session)  # Pass the session to MCP service with error handling
        self.tool_registry = get_tool_registry(self.mcp_service)  # Create tool registry with MCP service
    
    async def run_agent(self, user_id: str, message: str, conversation_id: UUID = None):
        """
        Run the AI agent with the provided message and conversation context
        """
        import time
        start_time = time.time()
        
        # Log the start of the agent operation
        log_conversation_event(
            event_type='agent_run_started',
            conversation_id=str(conversation_id) if conversation_id else 'new',
            user_id=user_id
        )
        
        # Get or create conversation
        if conversation_id:
            conversation = self.conversation_service.get_conversation_by_id(conversation_id)
            if not conversation:
                log_conversation_event(
                    event_type='conversation_not_found',
                    conversation_id=str(conversation_id),
                    user_id=user_id,
                    details={'error': f'Conversation with id {conversation_id} not found'}
                )
                raise ValueError(f"Conversation with id {conversation_id} not found")
        else:
            # Create a new conversation
            conversation = self.conversation_service.create_conversation(user_id)
            log_conversation_event(
                event_type='conversation_created',
                conversation_id=str(conversation.id),
                user_id=user_id,
                details={'title': conversation.title}
            )

        # Add user message to conversation
        user_message = self.conversation_service.create_message(
            conversation.id,
            "user",
            message
        )
        log_conversation_event(
            event_type='user_message_added',
            conversation_id=str(conversation.id),
            user_id=user_id,
            details={'message_length': len(message)}
        )

        # Build context from conversation history
        context = self.conversation_service.build_conversation_context(conversation.id)
        log_conversation_event(
            event_type='context_built',
            conversation_id=str(conversation.id),
            user_id=user_id,
            details={'context_size': len(context)}
        )

        # Prepare messages for the AI agent
        messages = [
            {"role": "system", "content": TASK_MANAGEMENT_AGENT_PROMPT}
        ]

        # Add conversation history
        for ctx_msg in context:
            messages.append(ctx_msg)

        # Update conversation title if it's not set and this is the first message
        if not conversation.title and len(context) == 1:
            # Extract a short title from the first user message
            first_user_message = next((msg for msg in context if msg["role"] == "user"), None)
            if first_user_message:
                title = first_user_message["content"][:50]  # Take first 50 chars as title
                self.conversation_service.update_conversation_title(conversation.id, title)
                log_conversation_event(
                    event_type='conversation_title_updated',
                    conversation_id=str(conversation.id),
                    user_id=user_id,
                    details={'new_title': title}
                )

        # Get tools from the registry
        tools = self.tool_registry.get_all_tools()

        # Call the OpenAI API with function calling
        try:
            openai_start_time = time.time()
            response = await client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            openai_duration = (time.time() - openai_start_time) * 1000  # Convert to milliseconds

            # Process the response
            response_message = response.choices[0].message

            # If the agent wants to call a tool
            tool_calls = response_message.tool_calls
            if tool_calls:
                # Execute the tool calls
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Log the tool call
                    log_tool_call(
                        tool_name=function_name,
                        conversation_id=str(conversation.id),
                        user_id=user_id,
                        input_params=function_args
                    )
                    
                    tool_start_time = time.time()
                    
                    # Execute the appropriate MCP service function
                    try:
                        if function_name == "create_task":
                            result = await self.mcp_service.create_task(
                                title=function_args.get("title"),
                                description=function_args.get("description"),
                                user_id=user_id
                            )
                        elif function_name == "update_task":
                            result = await self.mcp_service.update_task(
                                task_id=function_args.get("task_id"),
                                title=function_args.get("title"),
                                description=function_args.get("description"),
                                status=function_args.get("status")
                            )
                        elif function_name == "delete_task":
                            result = await self.mcp_service.delete_task(
                                task_id=function_args.get("task_id")
                            )
                        elif function_name == "list_tasks":
                            result = await self.mcp_service.list_tasks(
                                user_id=user_id,
                                status=function_args.get("status")
                            )
                        else:
                            result = {"error": f"Unknown function: {function_name}", "success": False}
                    except Exception as e:
                        # Handle any unexpected errors during tool execution
                        result = {
                            "success": False,
                            "error": str(e),
                            "message": "An error occurred while executing the task operation."
                        }
                        print(f"Unexpected error in tool execution: {str(e)}")
                        
                        # Log the tool call failure
                        log_tool_call(
                            tool_name=function_name,
                            conversation_id=str(conversation.id),
                            user_id=user_id,
                            input_params=function_args,
                            output_result=result,
                            duration_ms=(time.time() - tool_start_time) * 1000,
                            success=False,
                            error_details={"exception": str(e)}
                        )
                        continue  # Continue with other tool calls if possible

                    # Log the successful tool call
                    log_tool_call(
                        tool_name=function_name,
                        conversation_id=str(conversation.id),
                        user_id=user_id,
                        input_params=function_args,
                        output_result=result,
                        duration_ms=(time.time() - tool_start_time) * 1000,
                        success=result.get("success", True)
                    )

                    # Add tool response to messages for the next API call
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(result),
                        "tool_call_id": tool_call.id
                    })

                # Get the final response from the agent after tool execution
                final_openai_start_time = time.time()
                final_response = await client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=messages
                )
                final_openai_duration = (time.time() - final_openai_start_time) * 1000  # Convert to milliseconds
                final_content = final_response.choices[0].message.content
            else:
                # No tool calls, just return the agent's response
                final_content = response_message.content
                openai_duration = (time.time() - openai_start_time) * 1000  # Convert to milliseconds

            # Add assistant response to conversation
            assistant_message = self.conversation_service.create_message(
                conversation.id,
                "assistant",
                final_content
            )
            log_conversation_event(
                event_type='assistant_message_added',
                conversation_id=str(conversation.id),
                user_id=user_id,
                details={'message_length': len(final_content) if final_content else 0}
            )

            # Calculate total duration
            total_duration = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Record performance metric
            record_response_time(total_duration, 'chat_process')
            
            # Log the successful agent operation
            log_agent_operation(
                operation_type='chat_process',
                conversation_id=str(conversation.id),
                user_id=user_id,
                input_message=message,
                output_message=final_content,
                duration_ms=total_duration,
                success=True
            )

            # Return the response and conversation ID
            return {
                "conversation_id": str(conversation.id),
                "response": final_content,
                "tool_calls_executed": bool(tool_calls)
            }

        except Exception as e:
            # Calculate duration before error
            total_duration = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Record performance metric for error case
            record_response_time(total_duration, 'chat_process')
            record_error(type(e).__name__, 'chat_process')
            
            # Handle any errors that occur during agent execution
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in agent execution: {error_details}")  # Log for debugging

            # Import error response utilities
            from ..services.error_responses import create_error_response, ErrorCode
            
            # Create a user-friendly error response
            error_response = create_error_response(
                error_code=ErrorCode.INTERNAL_ERROR,
                message=f"An error occurred while processing your request: {str(e)}",
                details={
                    "error_type": type(e).__name__,
                    "traceback": error_details
                },
                user_friendly_message="I encountered an issue while processing your request. Please try again or rephrase your request."
            )

            error_message = error_response["user_message"]

            # Add error message to conversation
            error_assistant_message = self.conversation_service.create_message(
                conversation.id,
                "assistant",
                error_message
            )

            # Log the failed agent operation
            log_agent_operation(
                operation_type='chat_process',
                conversation_id=str(conversation.id),
                user_id=user_id,
                input_message=message,
                output_message=error_message,
                duration_ms=total_duration,
                success=False,
                error_details={"exception": str(e), "traceback": error_details}
            )

            return {
                "conversation_id": str(conversation.id),
                "response": error_message,
                "error": True,
                "error_details": error_response  # Include full error details for debugging if needed
            }


