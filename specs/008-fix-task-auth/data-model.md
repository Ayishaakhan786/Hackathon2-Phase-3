# Data Model: Task Management for Hackathon Mode

## Entities

### Task
Represents a user task that can be created/retrieved without authentication during hackathon mode.

**Fields:**
- `id`: UUID (Primary Key, auto-generated)
- `title`: String (min_length=1, max_length=255) - Required
- `description`: String (optional, max_length=1000) - Nullable
- `completed`: Boolean (default=False) - Task completion status
- `due_date`: DateTime (optional) - Due date for the task
- `created_at`: DateTime (auto-generated) - Timestamp when task was created
- `updated_at`: DateTime (auto-generated) - Timestamp when task was last updated
- `user_id`: UUID (Foreign Key) - Associated user ID

**Relationships:**
- Belongs to one User (many-to-one relationship)
- User has many Tasks

**Validation Rules:**
- Title must be between 1 and 255 characters
- Description must not exceed 1000 characters if provided
- Completed field defaults to False
- Created_at and updated_at are automatically managed

### User
Identified by user_id in the path, but not authenticated during hackathon mode.

**Fields:**
- `id`: UUID (Primary Key, auto-generated)
- `email`: String (unique, max_length=255) - User's email address
- `first_name`: String (max_length=100) - User's first name
- `last_name`: String (max_length=100) - User's last name
- `password_hash`: String (max_length=255) - Hashed password
- `created_at`: DateTime (auto-generated) - Account creation timestamp
- `updated_at`: DateTime (auto-generated) - Last update timestamp

**Relationships:**
- Has many Tasks (one-to-many relationship)
- Tasks belong to one User

## State Transitions

### Task State Transitions
- `active` → `completed`: When user marks task as complete via PATCH /tasks/{id}/complete
- `completed` → `active`: When user unmarks task as complete via PATCH /tasks/{id}/complete

## API Contract Changes for Hackathon Mode

### Authentication Relaxation
During hackathon mode, the following endpoints will not require authentication:
- `POST /api/v1/tasks/{user_id}/tasks`
- `GET /api/v1/tasks/{user_id}/tasks`
- `GET /api/v1/tasks/{user_id}/tasks/{task_id}`
- `PUT /api/v1/tasks/{user_id}/tasks/{task_id}`
- `DELETE /api/v1/tasks/{user_id}/tasks/{task_id}`
- `PATCH /api/v1/tasks/{user_id}/tasks/{task_id}/complete`

### Validation Changes
- User ID validation will be bypassed during hackathon mode
- Direct access to any user's tasks will be possible during hackathon mode (for development purposes)
- Normal user ownership validation will be restored in production mode