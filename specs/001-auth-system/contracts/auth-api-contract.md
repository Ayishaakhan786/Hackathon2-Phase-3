# Authentication API Contracts

**Date**: 2026-02-06
**Feature**: Authentication & User Foundation
**Branch**: 001-auth-system

## Overview

This document defines the API contracts for the authentication system, specifying the endpoints, request/response formats, and authentication requirements.

## Base Path

All authentication-related endpoints will follow the pattern:
`/api/v1/auth`

## Authentication Endpoints

### 1. User Registration

**Endpoint**: `POST /api/v1/auth/register`

**Description**: Creates a new user account

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
- Success (201 Created):
  ```json
  {
    "success": true,
    "message": "User registered successfully",
    "user": {
      "id": "uuid-string",
      "email": "user@example.com",
      "created_at": "2026-02-06T10:00:00Z"
    }
  }
  ```
- Error (400 Bad Request):
  ```json
  {
    "success": false,
    "message": "Validation error",
    "errors": [
      {"field": "email", "message": "Invalid email format"},
      {"field": "password", "message": "Password too weak"}
    ]
  }
  ```
- Error (409 Conflict):
  ```json
  {
    "success": false,
    "message": "Email already registered"
  }
  ```

### 2. User Login

**Endpoint**: `POST /api/v1/auth/login`

**Description**: Authenticates a user and returns JWT token

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
    "success": true,
    "message": "Login successful",
    "access_token": "jwt-token-string",
    "token_type": "bearer",
    "expires_in": 900
  }
  ```
- Error (401 Unauthorized):
  ```json
  {
    "success": false,
    "message": "Invalid credentials"
  }
  ```

### 3. User Logout

**Endpoint**: `POST /api/v1/auth/logout`

**Description**: Logs out the current user

**Authentication**: Required (valid JWT token)

**Request**:
- Headers: `Authorization: Bearer {access_token}`

**Response**:
- Success (200 OK):
  ```json
  {
    "success": true,
    "message": "Logout successful"
  }
  ```

### 4. Get Current User

**Endpoint**: `GET /api/v1/auth/me`

**Description**: Retrieves information about the currently authenticated user

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
    "success": false,
    "message": "Not authenticated"
  }
  ```

### 5. Refresh Token

**Endpoint**: `POST /api/v1/auth/refresh`

**Description**: Refreshes the access token using a refresh token

**Request**:
- Headers: `Content-Type: application/json`
- Body:
  ```json
  {
    "refresh_token": "refresh-token-string"
  }
  ```

**Response**:
- Success (200 OK):
  ```json
  {
    "success": true,
    "message": "Token refreshed successfully",
    "access_token": "new-jwt-token-string",
    "token_type": "bearer",
    "expires_in": 900
  }
  ```
- Error (401 Unauthorized):
  ```json
  {
    "success": false,
    "message": "Invalid or expired refresh token"
  }
  ```

## User-Specific Endpoints (Require User Ownership Validation)

### 6. Get User Profile

**Endpoint**: `GET /api/v1/users/{user_id}`

**Description**: Retrieves profile information for a specific user

**Authentication**: Required (valid JWT token)
**Authorization**: User must be the same as the requested user_id

**Request**:
- Headers: `Authorization: Bearer {access_token}`
- Path Parameter: `user_id` (the UUID of the user to retrieve)

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
    "success": false,
    "message": "Not authenticated"
  }
  ```
- Error (403 Forbidden):
  ```json
  {
    "success": false,
    "message": "Access forbidden: cannot access other user's profile"
  }
  ```
- Error (404 Not Found):
  ```json
  {
    "success": false,
    "message": "User not found"
  }
  ```

## Common Error Responses

For all endpoints, the following error responses may occur:

- **401 Unauthorized**: No valid authentication token provided
- **403 Forbidden**: Valid token but insufficient permissions
- **422 Unprocessable Entity**: Request validation failed
- **500 Internal Server Error**: Unexpected server error

## Security Considerations

1. All authentication-related endpoints must use HTTPS
2. Passwords must never be returned in any response
3. JWT tokens should have short expiration times
4. All user-specific endpoints must validate ownership
5. Rate limiting should be applied to authentication endpoints