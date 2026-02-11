# Data Model: MCP Task Management Tools

## Entities

### Task
Represents a user's task with unique identifier, associated user, title, description, completion status, and timestamps for creation and last update.

**Fields**:
- `id` (UUID/string): Unique identifier for the task
- `user_id` (string): Identifier for the user who owns the task
- `title` (string): Title of the task (required)
- `description` (string): Optional description of the task
- `completed` (boolean): Flag indicating if the task is completed (default: false)
- `created_at` (datetime): Timestamp when the task was created
- `updated_at` (datetime): Timestamp when the task was last updated

**Validation Rules**:
- `user_id` is required and must be a valid user identifier
- `title` is required and must not be empty
- `completed` defaults to false when creating a new task
- `created_at` is set automatically on creation
- `updated_at` is updated automatically on any modification

## Relationships

None applicable for this single entity model as it represents a standalone task record.

## State Transitions

- `completed` field: `false` → `true` (once a task is completed, it typically remains completed)