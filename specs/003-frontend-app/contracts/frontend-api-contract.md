# Frontend API Integration Contracts

**Date**: 2026-02-06
**Feature**: Frontend Application & User Experience
**Branch**: 003-frontend-app

## Overview

This document defines the API contracts for the frontend integration with the backend APIs. It specifies the expected request/response formats and error handling patterns that the frontend needs to implement.

## Base Configuration

### API Base URL
- Production: `https://api.yourdomain.com/api/v1`
- Development: `http://localhost:8000/api/v1`
- Configurable via environment variables

### Authentication Headers
All authenticated requests must include:
```
Authorization: Bearer {jwt_token}
```

## Authentication Endpoints

### 1. User Login

**Endpoint**: `POST /auth/login`

**Request**:
- Headers: `Content-Type: application/json`
- Body:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```

**Response**:
- Success (200 OK):
  ```json
  {
    "access_token": "jwt-token-string",
    "token_type": "bearer",
    "expires_in": 900
  }
  ```
- Error (401 Unauthorized):
  ```json
  {
    "detail": "Incorrect email or password"
  }
  ```

### 2. User Registration

**Endpoint**: `POST /auth/register`

**Request**:
- Headers: `Content-Type: application/json`
- Body:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123",
    "confirm_password": "securePassword123"
  }
  ```

**Response**:
- Success (200 OK):
  ```json
  {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-02-06T10:00:00Z",
    "updated_at": "2026-02-06T10:00:00Z",
    "is_active": true,
    "is_verified": false
  }
  ```
- Error (400 Bad Request):
  ```json
  {
    "detail": "Validation error",
    "errors": [
      {"field": "email", "message": "Invalid email format"},
      {"field": "password", "message": "Password too weak"}
    ]
  }
  ```
- Error (409 Conflict):
  ```json
  {
    "detail": "Email already registered"
  }
  ```

### 3. Get Current User

**Endpoint**: `GET /auth/me`

**Authentication**: Required (valid JWT token)

**Request**:
- Headers: `Authorization: Bearer {access_token}`

**Response**:
- Success (200 OK):
  ```json
  {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-02-06T10:00:00Z",
    "updated_at": "2026-02-06T10:00:00Z",
    "is_active": true,
    "is_verified": false
  }
  ```
- Error (401 Unauthorized):
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```

## Task Management Endpoints

### 1. List User's Tasks

**Endpoint**: `GET /tasks/{user_id}`

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

**Endpoint**: `POST /tasks/{user_id}`

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

**Endpoint**: `GET /tasks/{user_id}/{task_id}`

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

**Endpoint**: `PUT /tasks/{user_id}/{task_id}`

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

**Endpoint**: `DELETE /tasks/{user_id}/{task_id}`

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

**Endpoint**: `PATCH /tasks/{user_id}/{task_id}/complete`

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

## Frontend Implementation Requirements

### Loading States
- Show loading indicators during API requests
- Disable form inputs during submission
- Implement skeleton loading for content areas

### Error Handling
- Display user-friendly error messages
- Implement error boundaries for unexpected errors
- Provide retry mechanisms for failed requests
- Log errors appropriately for debugging

### Caching Strategy
- Cache user profile data
- Cache task lists with appropriate invalidation
- Implement optimistic updates for better UX

### Token Management
- Store JWT tokens securely
- Implement automatic token refresh
- Handle token expiration gracefully
- Redirect to login when authentication fails