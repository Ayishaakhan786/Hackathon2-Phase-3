# Data Model: Frontend Main Page UI — Todo Application

## Task Entity

**Description**: Represents a single todo item in the UI

**Fields**:
- `id`: string | unique identifier for the task
- `title`: string | text content of the task
- `completed`: boolean | completion status of the task
- `createdAt`: Date | timestamp when the task was created (for potential future use)

**Validation Rules**:
- `title` must not be empty or contain only whitespace
- `id` must be unique within the task list

**State Transitions**:
- Pending (completed: false) → Completed (completed: true) when user toggles checkbox
- Completed (completed: true) → Pending (completed: false) when user toggles checkbox

## Task List Entity

**Description**: Collection of tasks displayed on the main page

**Fields**:
- `tasks`: Array<Task> | list of all tasks
- `filter`: string | current filter applied (all, active, completed) - for potential future use

**Operations**:
- Add task: Insert new Task object to the list
- Update task: Modify existing Task properties (title, completed)
- Delete task: Remove Task object from the list