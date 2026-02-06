# Data Model: Frontend Structure & Components

**Date**: 2026-02-06
**Feature**: Frontend Reset & Proper Next.js Initialization
**Branch**: 004-frontend-reset

## Overview

This document defines the frontend structure and components for the Next.js application. Since this is a frontend reset task, the "data model" refers to the component architecture and UI entities rather than backend data entities.

## Page Entities

### Root Layout (app/layout.tsx)
- **Purpose**: Global layout shared across all pages
- **Attributes**: 
  - Children (ReactNode)
  - Global styles and providers
- **Relationships**: Contains all other pages and layouts

### Home Page (app/page.tsx)
- **Purpose**: Main landing page for the application
- **Attributes**:
  - Page content and components
  - Navigation links
- **Relationships**: Child of Root Layout

## Component Entities

### Header Component (components/layout/Header.tsx)
- **Purpose**: Site-wide header with navigation
- **Attributes**:
  - Logo/branding
  - Navigation links
  - User authentication status
- **Relationships**: Used in Root Layout

### Sidebar Component (components/layout/Sidebar.tsx)
- **Purpose**: Secondary navigation and quick actions
- **Attributes**:
  - Menu items
  - User profile section
- **Relationships**: Used in Root Layout or specific pages

### Footer Component (components/layout/Footer.tsx)
- **Purpose**: Site-wide footer with additional links
- **Attributes**:
  - Copyright information
  - Additional navigation links
  - Social media links
- **Relationships**: Used in Root Layout

### Task Card Component (components/tasks/TaskCard.tsx)
- **Purpose**: Display individual task information
- **Attributes**:
  - Task title
  - Task description
  - Completion status
  - Due date
  - Action buttons (edit, delete, toggle completion)
- **Relationships**: Used in Task List component

### Task List Component (components/tasks/TaskList.tsx)
- **Purpose**: Display multiple tasks in a list
- **Attributes**:
  - Array of Task Cards
  - Filtering options
  - Sorting options
- **Relationships**: Contains multiple Task Card components

### Task Form Component (components/tasks/TaskForm.tsx)
- **Purpose**: Create or edit task information
- **Attributes**:
  - Input fields for task properties
  - Validation messages
  - Submit/cancel buttons
- **Relationships**: Used in task creation and editing pages

### Task Detail Component (components/tasks/TaskDetail.tsx)
- **Purpose**: Display detailed task information
- **Attributes**:
  - Task title
  - Task description
  - Completion status
  - Due date
  - Creation/update timestamps
- **Relationships**: Used in task detail page

## State Management Entities

### Task State (store/tasks.ts or hooks/useTasks.ts)
- **Purpose**: Manage task-related state
- **Attributes**:
  - List of tasks
  - Loading state
  - Error state
  - Current task (for detail view)
- **Operations**:
  - Fetch tasks
  - Create task
  - Update task
  - Delete task
  - Toggle completion

### Authentication State (store/auth.ts or hooks/useAuth.ts)
- **Purpose**: Manage user authentication state
- **Attributes**:
  - User session data
  - Loading state
  - Error state
- **Operations**:
  - Login
  - Logout
  - Register
  - Token management

## API Integration Entities

### Task API Service (lib/api/tasks.ts)
- **Purpose**: Handle task-related API operations
- **Methods**:
  - getTasks(userId)
  - getTask(userId, taskId)
  - createTask(userId, taskData)
  - updateTask(userId, taskId, taskData)
  - deleteTask(userId, taskId)
  - toggleTaskCompletion(userId, taskId)

### Authentication API Service (lib/api/auth.ts)
- **Purpose**: Handle authentication-related API operations
- **Methods**:
  - login(credentials)
  - register(userData)
  - logout()
  - getCurrentUser()

## Validation Rules

### Task Validation
- Title must be provided and not exceed 255 characters
- Description must not exceed 1000 characters if provided
- Due date must be a valid future date if provided
- User ID must match authenticated user

### Form Validation
- All required fields must be filled
- Email format must be valid for authentication forms
- Passwords must meet minimum security requirements
- Form submissions must be validated before API calls

## State Transitions

### Task State Transitions
1. **Initial State**: Empty task list, loading = false, error = null
2. **Loading State**: Loading = true, fetching tasks from API
3. **Loaded State**: Loading = false, tasks populated, error = null
4. **Error State**: Loading = false, tasks = [], error = error message
5. **Updated State**: Task modified in the list after API response

### Authentication State Transitions
1. **Uninitialized**: Checking for existing session
2. **Loading**: Verifying authentication status
3. **Authenticated**: User is logged in with valid session
4. **Unauthenticated**: User is not logged in
5. **Error**: Authentication error occurred

## Constraints

### Frontend Constraints
- All components must follow Next.js App Router conventions
- Components must be responsive and mobile-friendly
- Forms must have proper validation and error handling
- API calls must handle loading and error states
- Authentication state must be preserved across page navigations

### Performance Constraints
- Initial page load should be under 3 seconds
- Interactive elements should respond within 100ms
- Components should be optimized for performance
- Images should be properly optimized
- Bundle size should be minimized

### Security Constraints
- Authentication tokens must be stored securely
- User data isolation must be maintained
- Input validation must be performed before API calls
- Sensitive information must not be exposed in client-side code
- API calls must be properly authenticated