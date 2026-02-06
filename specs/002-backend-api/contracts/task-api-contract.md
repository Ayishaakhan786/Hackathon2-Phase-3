# Task Management API Contracts

**Date**: 2026-02-06
**Feature**: Backend API & Database
**Branch**: 002-backend-api

## Overview

This document defines the API contracts for the task management system, specifying the endpoints, request/response formats, and authentication requirements.

## Base Path

All task-related endpoints will follow the pattern:
`/api/{user_id}/tasks`

Where `{user_id}` is the UUID of the authenticated user.

## Task Management Endpoints

### 1. List User's Tasks

**Endpoint**: `GET /api/{user_id}/tasks`

**Description**: Retrieves all tasks belonging to the specified user

**Authentication**: Required (valid JWT token)

**Request**:
- Headers: `Authorization: Bearer {access_token}`
- Path Parameter: `user_id` (the UUID of the user whose tasks to retrieve)

**Response**:
- Success (200 OK):
  ```json
  [
    {
      "id": "uuid-string",
      "title": "Sample Task",
      "description": "Detailed description of the task",
      "completed": false,
      "due_date": "2026-12-31T23:59:59Z",
      "created_at": "2026-02-06T10:00:00Z",
      "updated_at": "2026-02-06T10:00:00Z",
      "user_id": "user-uuid-string"
    },
    {
      "id": "another-uuid-string",
      "title": "Another Task",
      "description": "Another task description",
      "completed": true,
      "due_date": null,
      "created_at": "2026-02-06T09:00:00Z",
      "updated_at": "2026-02-06T11:30:00Z",
      "user_id": "user-uuid-string"
    }
  ]
  ```
- Error (401 Unauthorized):
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- Error (403 Forbidden):
  ```json
  {
    "detail": "Access forbidden: cannot access other user's tasks"
  }
  ```

### 2. Create a Task

**Endpoint**: `POST /api/{user_id}/tasks`

**Description**: Creates a new task for the specified user

**Authentication**: Required (valid JWT token)

**Request**:
- Headers: `Authorization: Bearer {access_token}`
- Path Parameter: `user_id` (the UUID of the user to create the task for)
- Body:
  ```json
  {
    "title": "New Task",
    "description": "Description of the new task",
    "due_date": "2026-12-31T23:59:59Z"
  }
  ```

**Response**:
- Success (201 Created):
  ```json
  {
    "id": "new-task-uuid-string",
    "title": "New Task",
    "description": "Description of the new task",
    "completed": false,
    "due_date": "2026-12-31T23:59:59Z",
    "created_at": "2026-02-06T10:00:00Z",
    "updated_at": "2026-02-06T10:00:00Z",
    "user_id": "user-uuid-string"
  }
  ```
- Error (400 Bad Request):
  ```json
  {
    "detail": "Validation error"
  }
  ```
- Error (401 Unauthorized):
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- Error (403 Forbidden):
  ```json
  {
    "detail": "Access forbidden: cannot create tasks for other users"
  }
  ```

### 3. Get Task Details

**Endpoint**: `GET /api/{user_id}/tasks/{task_id}`

**Description**: Retrieves details of a specific task

**Authentication**: Required (valid JWT token)

**Request**:
- Headers: `Authorization: Bearer {access_token}`
- Path Parameters:
  - `user_id` (the UUID of the user who owns the task)
  - `task_id` (the UUID of the task to retrieve)

**Response**:
- Success (200 OK):
  ```json
  {
    "id": "task-uuid-string",
    "title": "Sample Task",
    "description": "Detailed description of the task",
    "completed": false,
    "due_date": "2026-12-31T23:59:59Z",
    "created_at": "2026-02-06T10:00:00Z",
    "updated_at": "2026-02-06T10:00:00Z",
    "user_id": "user-uuid-string"
  }
  ```
- Error (401 Unauthorized):
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- Error (403 Forbidden):
  ```json
  {
    "detail": "Access forbidden: cannot access other user's tasks"
  }
  ```
- Error (404 Not Found):
  ```json
  {
    "detail": "Task not found"
  }
  ```

### 4. Update a Task

**Endpoint**: `PUT /api/{user_id}/tasks/{task_id}`

**Description**: Updates details of a specific task

**Authentication**: Required (valid JWT token)

**Request**:
- Headers: `Authorization: Bearer {access_token}`
- Path Parameters:
  - `user_id` (the UUID of the user who owns the task)
  - `task_id` (the UUID of the task to update)
- Body:
  ```json
  {
    "title": "Updated Task Title",
    "description": "Updated description of the task",
    "due_date": "2026-12-31T23:59:59Z"
  }
  ```

**Response**:
- Success (200 OK):
  ```json
  {
    "id": "task-uuid-string",
    "title": "Updated Task Title",
    "description": "Updated description of the task",
    "completed": false,
    "due_date": "2026-12-31T23:59:59Z",
    "created_at": "2026-02-06T10:00:00Z",
    "updated_at": "2026-02-06T11:00:00Z",
    "user_id": "user-uuid-string"
  }
  ```
- Error (400 Bad Request):
  ```json
  {
    "detail": "Validation error"
  }
  ```
- Error (401 Unauthorized):
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- Error (403 Forbidden):
  ```json
  {
    "detail": "Access forbidden: cannot update other user's tasks"
  }
  ```
- Error (404 Not Found):
  ```json
  {
    "detail": "Task not found"
  }
  ```

### 5. Delete a Task

**Endpoint**: `DELETE /api/{user_id}/tasks/{task_id}`

**Description**: Deletes a specific task

**Authentication**: Required (valid JWT token)

**Request**:
- Headers: `Authorization: Bearer {access_token}`
- Path Parameters:
  - `user_id` (the UUID of the user who owns the task)
  - `task_id` (the UUID of the task to delete)

**Response**:
- Success (204 No Content): Task successfully deleted
- Error (401 Unauthorized):
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- Error (403 Forbidden):
  ```json
  {
    "detail": "Access forbidden: cannot delete other user's tasks"
  }
  ```
- Error (404 Not Found):
  ```json
  {
    "detail": "Task not found"
  }
  ```

### 6. Toggle Task Completion

**Endpoint**: `PATCH /api/{user_id}/tasks/{task_id}/complete`

**Description**: Toggles the completion status of a specific task

**Authentication**: Required (valid JWT token)

**Request**:
- Headers: `Authorization: Bearer {access_token}`
- Path Parameters:
  - `user_id` (the UUID of the user who owns the task)
  - `task_id` (the UUID of the task to update)
- Body (optional):
  ```json
  {
    "completed": true
  }
  ```

**Response**:
- Success (200 OK):
  ```json
  {
    "id": "task-uuid-string",
    "title": "Sample Task",
    "description": "Detailed description of the task",
    "completed": true,
    "due_date": "2026-12-31T23:59:59Z",
    "created_at": "2026-02-06T10:00:00Z",
    "updated_at": "2026-02-06T11:00:00Z",
    "user_id": "user-uuid-string"
  }
  ```
- Error (401 Unauthorized):
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- Error (403 Forbidden):
  ```json
  {
    "detail": "Access forbidden: cannot update other user's tasks"
  }
  ```
- Error (404 Not Found):
  ```json
  {
    "detail": "Task not found"
  }
  ```

## Common Error Responses

For all endpoints, the following error responses may occur:

- **401 Unauthorized**: No valid authentication token provided
- **403 Forbidden**: Valid token but insufficient permissions (user mismatch)
- **404 Not Found**: Requested resource does not exist
- **422 Unprocessable Entity**: Request validation failed
- **500 Internal Server Error**: Unexpected server error

## Security Considerations

1. All endpoints require JWT authentication
2. User ID in the token must match the user_id in the URL path
3. Users can only access their own tasks
4. All sensitive data should be properly validated and sanitized
5. Rate limiting should be applied to prevent abuse