# Quickstart Guide: Task API Without Authentication (Hackathon Mode)

## Overview
This guide explains how to use the Task API endpoints without authentication during hackathon mode.

## Prerequisites
- Backend service running on `http://localhost:8000`
- No authentication token required during hackathon mode

## Available Endpoints

### 1. Create a Task
**Endpoint:** `POST /api/v1/tasks/{user_id}/tasks`

**Description:** Creates a new task for the specified user.

**Request Body:**
```json
{
  "title": "string (required, 1-255 chars)",
  "description": "string (optional, max 1000 chars)",
  "completed": "boolean (optional, default: false)",
  "due_date": "string (optional, ISO 8601 format)"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/123e4567-e89b-12d3-a456-426614174000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project proposal",
    "description": "Write and submit the project proposal document",
    "due_date": "2026-02-15T10:00:00Z"
  }'
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "title": "Complete project proposal",
  "description": "Write and submit the project proposal document",
  "completed": false,
  "due_date": "2026-02-15T10:00:00Z",
  "created_at": "2026-02-06T10:00:00Z",
  "updated_at": "2026-02-06T10:00:00Z",
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### 2. List User Tasks
**Endpoint:** `GET /api/v1/tasks/{user_id}/tasks`

**Description:** Retrieves all tasks for the specified user.

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/123e4567-e89b-12d3-a456-426614174000/tasks"
```

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "due_date": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "user_id": "uuid"
  }
]
```

### 3. Get Specific Task
**Endpoint:** `GET /api/v1/tasks/{user_id}/tasks/{task_id}`

**Description:** Retrieves a specific task by ID.

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/123e4567-e89b-12d3-a456-426614174000/tasks/987e6543-e21b-43d5-a678-987654321000"
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "due_date": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "user_id": "uuid"
}
```

### 4. Update Task
**Endpoint:** `PUT /api/v1/tasks/{user_id}/tasks/{task_id}`

**Description:** Updates a specific task by ID.

**Request Body:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (optional)",
  "due_date": "string (optional)"
}
```

**Example Request:**
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/123e4567-e89b-12d3-a456-426614174000/tasks/987e6543-e21b-43d5-a678-987654321000" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "description": "Updated description",
    "completed": true
  }'
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true,
  "due_date": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "user_id": "uuid"
}
```

### 5. Delete Task
**Endpoint:** `DELETE /api/v1/tasks/{user_id}/tasks/{task_id}`

**Description:** Deletes a specific task by ID.

**Example Request:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/123e4567-e89b-12d3-a456-426614174000/tasks/987e6543-e21b-43d5-a678-987654321000"
```

**Response:** `204 No Content`

### 6. Toggle Task Completion
**Endpoint:** `PATCH /api/v1/tasks/{user_id}/tasks/{task_id}/complete`

**Description:** Toggles the completion status of a specific task.

**Example Request:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/123e4567-e89b-12d3-a456-426614174000/tasks/987e6543-e21b-43d5-a678-987654321000/complete"
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "completed": "boolean (toggled)",
  "due_date": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "user_id": "uuid"
}
```

## Important Notes for Hackathon Mode
- Authentication is disabled for task endpoints during hackathon mode
- No Authorization header is required
- User ID validation is bypassed (anyone can access any user's tasks)
- This is only for development/testing purposes
- Authentication will be re-enabled in production