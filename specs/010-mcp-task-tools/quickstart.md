# Quickstart Guide: MCP Task Management Tools

## Overview
This guide explains how to set up and use the MCP server for task management tools. The server exposes stateless tools that can be called by AI agents to perform task operations, with all data persisted in Neon PostgreSQL.

## Prerequisites
- Python 3.9+
- Poetry (dependency manager)
- Neon PostgreSQL database instance

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy the environment template
cp .env.example .env

# Update the database connection string in .env
DATABASE_URL="postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname"
```

### 2. Install Dependencies
```bash
poetry install
poetry shell
```

### 3. Initialize Database Tables
```bash
# Run the database initialization script
python -m src.db.init_tables
```

## MCP Server Usage

### Starting the MCP Server
```bash
# Run the MCP server
python -m src.mcp.server
```

### Using the MCP Tools

#### Adding a Task
```python
# Example of how an AI agent would call the add_task tool
result = await mcp_client.call_tool("add_task", {
    "user_id": "user123",
    "title": "Buy groceries",
    "description": "Milk, bread, eggs, and fruits"
})
```

#### Listing Tasks
```python
# Example of how an AI agent would call the list_tasks tool
result = await mcp_client.call_tool("list_tasks", {
    "user_id": "user123",
    "status": "pending"  # Optional: all, pending, completed
})
```

#### Completing a Task
```python
# Example of how an AI agent would call the complete_task tool
result = await mcp_client.call_tool("complete_task", {
    "user_id": "user123",
    "task_id": "task456"
})
```

#### Updating a Task
```python
# Example of how an AI agent would call the update_task tool
result = await mcp_client.call_tool("update_task", {
    "user_id": "user123",
    "task_id": "task456",
    "title": "Buy weekly groceries",
    "description": "Milk, bread, eggs, fruits, and vegetables"
})
```

#### Deleting a Task
```python
# Example of how an AI agent would call the delete_task tool
result = await mcp_client.call_tool("delete_task", {
    "user_id": "user123",
    "task_id": "task456"
})
```

## Expected Response Format
All MCP tools return responses in the following format:
```json
{
  "success": boolean,
  "message": string,
  "data": {}  // Optional field for additional data
}
```

## Key Components

### Models
- `Task`: Manages task data with user ownership and timestamps

### Services
- `TaskService`: Handles all task-related operations with database persistence

### MCP Server
- `MCPTaskServer`: Implements the MCP protocol and exposes task tools
- `TaskTools`: Contains the implementation of each task operation