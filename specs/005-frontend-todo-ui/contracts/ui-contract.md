# UI Contract: Todo Application Main Page

## Component: TodoPage

### Props
- None required

### State
- `tasks`: Array<TodoItem> - list of all tasks
- `newTaskTitle`: string - current value of the input field for new tasks

### Events/Callbacks
- `onAddTask(title: string)`: called when user submits a new task
- `onToggleTask(id: string)`: called when user toggles task completion
- `onDeleteTask(id: string)`: called when user deletes a task

## Component: TodoItem

### Props
- `id`: string - unique identifier for the task
- `title`: string - text content of the task
- `completed`: boolean - completion status
- `onToggle`: () => void - callback when user toggles completion
- `onDelete`: () => void - callback when user deletes the task

### Visual States
- Default: Normal text color and opacity
- Completed: Strikethrough text with muted color/opacity

## UI Elements

### Task Input Section
- Text input field with placeholder "Enter a new task..."
- Submit button labeled "Add Task"
- On submission, clears the input field

### Task List Section
- Displays all tasks in a list
- Each task shows:
  - Checkbox to toggle completion
  - Task title text
  - Delete button/icon
- Completed tasks have visual indication (strikethrough, muted color)

## Responsive Behavior
- On mobile: Vertical stacking of elements with appropriate padding
- On desktop: More spacious layout with horizontal arrangements where appropriate