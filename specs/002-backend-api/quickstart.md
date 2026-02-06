# Quickstart Guide: Backend API & Database

**Date**: 2026-02-06
**Feature**: Backend API & Database
**Branch**: 002-backend-api

## Overview

This guide provides a quick introduction to setting up and using the backend API and database for the task management application.

## Prerequisites

- Python 3.11+
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL database
- Completed authentication system (Spec 1)

## Setting Up the Environment

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-root>
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database and auth configurations
```

## Configuration

### Backend Configuration

1. Set up your database connection in `backend/.env`:
   ```
   DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
   ```

2. Configure JWT settings (should match Spec 1):
   ```
   SECRET_KEY=your-super-secret-key-from-spec1
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Running the Application

### 1. Start the Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## Using the Task Management API

### 1. Prerequisites

Before using the task management endpoints, you need to:
1. Register a user (from Spec 1)
2. Log in to obtain an access token (from Spec 1)

### 2. List User's Tasks

Send a GET request to `/api/{user_id}/tasks`:

```bash
curl -X GET http://localhost:8000/api/{your-user-id}/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 3. Create a Task

Send a POST request to `/api/{user_id}/tasks`:

```bash
curl -X POST http://localhost:8000/api/{your-user-id}/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Task",
    "description": "Description of the new task",
    "due_date": "2026-12-31T23:59:59Z"
  }'
```

### 4. Get Task Details

Send a GET request to `/api/{user_id}/tasks/{task_id}`:

```bash
curl -X GET http://localhost:8000/api/{your-user-id}/tasks/{task-id} \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 5. Update a Task

Send a PUT request to `/api/{user_id}/tasks/{task_id}`:

```bash
curl -X PUT http://localhost:8000/api/{your-user-id}/tasks/{task-id} \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Task Title",
    "description": "Updated description",
    "due_date": "2026-12-31T23:59:59Z"
  }'
```

### 6. Toggle Task Completion

Send a PATCH request to `/api/{user_id}/tasks/{task_id}/complete`:

```bash
curl -X PATCH http://localhost:8000/api/{your-user-id}/tasks/{task-id}/complete \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 7. Delete a Task

Send a DELETE request to `/api/{user_id}/tasks/{task_id}`:

```bash
curl -X DELETE http://localhost:8000/api/{your-user-id}/tasks/{task-id} \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## Testing the API

1. Create a user account using the authentication API
2. Log in to get an access token
3. Use the access token to make requests to the task management API
4. Verify that you can only access tasks belonging to your user ID
5. Test that unauthorized access attempts return 403 Forbidden

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Verify your `DATABASE_URL` in the backend `.env` file
2. **JWT Validation Errors**: Check that `SECRET_KEY` matches the one from Spec 1
3. **User ID Mismatch Errors**: Ensure the user_id in the URL matches the user_id in your JWT token
4. **CORS Issues**: Ensure your frontend URL is added to the CORS allowed origins in the backend

### Debugging API Calls

Enable debug logging in your environment files:
```
LOG_LEVEL=DEBUG
```

Check the application logs for authentication and authorization-related messages.