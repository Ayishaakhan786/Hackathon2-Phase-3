from typing import Dict, Any, Callable, Awaitable


class ToolRegistry:
    """
    Registry for MCP tools that can be used by the AI agent
    """
    
    def __init__(self, mcp_service):
        self.mcp_service = mcp_service
        self.tools = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """
        Register the default MCP tools based on the specification
        """
        self.register_tool(
            name="create_task",
            description="Create a new task",
            function=self._create_task_wrapper,
            parameters={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the task"},
                    "description": {"type": "string", "description": "Description of the task"}
                },
                "required": ["title"]
            }
        )
        
        self.register_tool(
            name="update_task",
            description="Update an existing task",
            function=self._update_task_wrapper,
            parameters={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of the task to update"},
                    "title": {"type": "string", "description": "New title of the task"},
                    "description": {"type": "string", "description": "New description of the task"},
                    "status": {"type": "string", "description": "New status of the task"}
                },
                "required": ["task_id"]
            }
        )
        
        self.register_tool(
            name="delete_task",
            description="Delete an existing task",
            function=self._delete_task_wrapper,
            parameters={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of the task to delete"}
                },
                "required": ["task_id"]
            }
        )
        
        self.register_tool(
            name="list_tasks",
            description="List tasks for the user",
            function=self._list_tasks_wrapper,
            parameters={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Filter tasks by status"}
                }
            }
        )
    
    def register_tool(
        self, 
        name: str, 
        description: str, 
        function: Callable[..., Awaitable[Dict[str, Any]]], 
        parameters: Dict[str, Any]
    ):
        """
        Register a new tool with the registry
        """
        self.tools[name] = {
            "name": name,
            "description": description,
            "function": function,
            "parameters": parameters
        }
    
    def get_tool(self, name: str):
        """
        Get a registered tool by name
        """
        return self.tools.get(name)
    
    def get_all_tools(self):
        """
        Get all registered tools in the format expected by OpenAI API
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            }
            for tool in self.tools.values()
        ]
    
    # Wrapper functions that call the MCP service
    async def _create_task_wrapper(self, title: str, description: str = None, user_id: str = None):
        return await self.mcp_service.create_task(title=title, description=description, user_id=user_id)
    
    async def _update_task_wrapper(self, task_id: str, title: str = None, description: str = None, status: str = None):
        return await self.mcp_service.update_task(task_id=task_id, title=title, description=description, status=status)
    
    async def _delete_task_wrapper(self, task_id: str):
        return await self.mcp_service.delete_task(task_id=task_id)
    
    async def _list_tasks_wrapper(self, user_id: str = None, status: str = None):
        return await self.mcp_service.list_tasks(user_id=user_id, status=status)


# Note: Global instance will be created when needed with the appropriate MCP service
def get_tool_registry(mcp_service):
    """
    Factory function to create a tool registry with an MCP service instance
    """
    return ToolRegistry(mcp_service)