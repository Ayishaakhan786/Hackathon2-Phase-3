# Data Model: Backend API & Database

**Date**: 2026-02-06
**Feature**: Backend API & Database
**Branch**: 002-backend-api

## Overview

This document defines the data models required for the task management backend, focusing on the Task entity and its relationship to the User entity from Spec 1.

## User Entity (from Spec 1)

### Attributes
- **id** (UUID): Unique identifier for the user
- **email** (String): User's email address (unique, required)
- **hashed_password** (String): BCrypt-hashed password (required)
- **created_at** (DateTime): Timestamp when the account was created
- **updated_at** (DateTime): Timestamp when the account was last updated
- **is_active** (Boolean): Whether the account is active (default: true)
- **is_verified** (Boolean): Whether the email has been verified (default: false)

### Relationships
- **Tasks** (one-to-many): A user can have many tasks

## Task Entity

### Attributes
- **id** (UUID): Unique identifier for the task
- **title** (String): Task title (required, max length: 255)
- **description** (Text): Detailed description of the task (optional)
- **completed** (Boolean): Whether the task is completed (default: false)
- **due_date** (DateTime): Optional deadline for the task
- **created_at** (DateTime): Timestamp when the task was created
- **updated_at** (DateTime): Timestamp when the task was last updated
- **user_id** (UUID): Foreign key linking to the user who owns this task

### Relationships
- **User** (many-to-one): The user who owns this task

### Validation Rules
- Title must be provided and not empty
- Title must be less than 255 characters
- Due date must be in the future if provided
- User ID must reference an existing user

## State Transitions

### Task States
1. **Incomplete** (Default): Task is created but not completed
2. **Completed**: Task has been marked as completed

### Transition Rules
- Incomplete → Completed: When user marks task as complete
- Completed → Incomplete: When user unmarks task as complete

## Constraints

### Data Integrity
- Task title cannot be null
- User ID must reference an existing user (foreign key constraint)
- Created_at and updated_at timestamps automatically managed
- Tasks cannot be created without a valid user reference

### Security
- Tasks can only be accessed by their owner
- Task ownership cannot be changed after creation
- Task IDs should be non-sequential to prevent enumeration attacks

## Indexes

### Required Indexes
- Index on user_id for efficient user-specific queries
- Index on completed for filtering completed/incomplete tasks
- Composite index on (user_id, completed) for common user-task queries
- Index on due_date for sorting and filtering by deadline