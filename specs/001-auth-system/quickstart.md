# Quickstart Guide: Authentication System

**Date**: 2026-02-06
**Feature**: Authentication & User Foundation
**Branch**: 001-auth-system

## Overview

This guide provides a quick introduction to setting up and using the authentication system for the multi-user task management application.

## Prerequisites

- Node.js 18+ for frontend
- Python 3.11+ for backend
- Neon Serverless PostgreSQL database
- Better Auth compatible environment

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

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API endpoints
```

## Configuration

### Backend Configuration

1. Set up your database connection in `backend/.env`:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   ```

2. Configure JWT settings:
   ```
   SECRET_KEY=your-super-secret-key-here
   ALGORITHM=RS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   ```

### Frontend Configuration

1. Configure API endpoints in `frontend/.env.local`:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
   ```

## Running the Application

### 1. Start the Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.main:app --reload --port 8000
```

### 2. Start the Frontend

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`.

## Using the Authentication System

### 1. Register a New User

Send a POST request to `/api/v1/auth/register`:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123",
    "confirm_password": "securePassword123"
  }'
```

### 2. Login

Send a POST request to `/api/v1/auth/login`:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123"
  }'
```

On successful login, you'll receive an access token.

### 3. Access Protected Resources

Include the access token in the Authorization header:

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 4. Logout

Send a POST request to `/api/v1/auth/logout`:

```bash
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## Testing the Authentication Flow

1. Register a new user
2. Log in with the registered credentials
3. Access the `/me` endpoint to verify authentication
4. Try accessing a protected resource without a token (should fail)
5. Try accessing another user's resource (should fail with 403)

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Verify your `DATABASE_URL` in the backend `.env` file
2. **JWT Validation Errors**: Check that `SECRET_KEY` is properly set and matches between services
3. **CORS Issues**: Ensure your frontend URL is added to the CORS allowed origins in the backend
4. **Token Expiration**: Access tokens expire after 15 minutes; implement refresh token logic for production

### Debugging Authentication

Enable debug logging in your environment files:
```
LOG_LEVEL=DEBUG
```

Check the application logs for authentication-related messages.