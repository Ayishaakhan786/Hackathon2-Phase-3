# Quickstart Guide: Frontend Application & User Experience

**Date**: 2026-02-02
**Feature**: Frontend Application & User Experience
**Branch**: 003-frontend-app

## Overview

This guide provides a quick introduction to setting up and using the frontend application for the task management system.

## Prerequisites

- Node.js 18+ 
- npm or yarn package manager
- Access to the backend API (from Spec 2)
- Completed authentication system (from Spec 1)

## Setting Up the Environment

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-root>
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local with your API endpoints and other configurations
```

## Configuration

### Frontend Configuration

1. Set up your API endpoint in `frontend/.env.local`:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
   NEXT_PUBLIC_APP_NAME=Task Manager
   ```

2. Configure authentication settings if needed:
   ```
   NEXT_PUBLIC_JWT_REFRESH_WINDOW=5 # Minutes before token expiry to refresh
   ```

## Running the Application

### 1. Start the Frontend

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`.

## Using the Frontend Application

### 1. Authentication Flows

#### Sign Up
1. Navigate to `/auth/signup`
2. Fill in the registration form with email and password
3. Submit the form to create a new account

#### Sign In
1. Navigate to `/auth/signin`
2. Enter your email and password
3. Submit the form to authenticate
4. You'll be redirected to the dashboard

#### Sign Out
1. Click the "Sign Out" button in the header
2. Your session will be cleared and you'll be redirected to the login page

### 2. Task Management Features

#### Viewing Tasks
1. After authentication, navigate to the dashboard or tasks page
2. Your tasks will be displayed in a list
3. Use filters to sort by completion status or date

#### Creating a Task
1. Click the "Create Task" button
2. Fill in the task details (title, description, due date)
3. Submit the form to create the task

#### Editing a Task
1. Click on a task to view its details
2. Click the "Edit" button
3. Update the task details
4. Save the changes

#### Completing a Task
1. Find the task in your list
2. Click the checkbox next to the task
3. The task's completion status will be toggled

#### Deleting a Task
1. Find the task in your list
2. Click the "Delete" button
3. Confirm the deletion in the modal

### 3. Responsive Behavior

The application is designed to work across different screen sizes:
- Mobile: Single-column layout with collapsible navigation
- Tablet: Two-column layout with sidebar navigation
- Desktop: Multi-column layout with full sidebar

## API Integration

### Making API Requests

The application uses a centralized API client that handles:
- JWT token attachment to requests
- Error handling and user feedback
- Loading states during requests
- Automatic retries for failed requests

### Authentication Flow

1. User credentials are sent to the backend for authentication
2. JWT token is received and stored securely
3. Token is attached to all subsequent API requests
4. Token is refreshed automatically before expiration
5. User is redirected to login if authentication fails

## Testing the Application

### Manual Testing

1. Complete the sign up flow
2. Sign in with your credentials
3. Create a few tasks
4. Update, complete, and delete tasks
5. Test the application on different screen sizes
6. Verify that unauthorized access is prevented

### Automated Testing

Run the test suite:
```bash
npm run test
```

Run end-to-end tests:
```bash
npm run e2e
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**: Verify your `NEXT_PUBLIC_API_BASE_URL` in the environment file
2. **Authentication Failures**: Check that the backend authentication service is running
3. **Token Expiration**: The application should handle this automatically, but you can force a refresh
4. **CORS Issues**: Ensure your backend allows requests from your frontend origin

### Debugging Frontend Issues

Enable debug logging in your environment file:
```
NEXT_PUBLIC_DEBUG=true
```

Check the browser console for JavaScript errors and network issues.