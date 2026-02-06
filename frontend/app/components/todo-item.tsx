import React from 'react';

// Define TypeScript interface for Task
export interface Task {
  id: string;
  title: string;
  completed: boolean;
  createdAt: Date;
}

interface TodoItemProps {
  task: Task;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ task, onToggle, onDelete }) => {
  return (
    <div 
      className={`flex flex-col sm:flex-row items-center justify-between p-3 border rounded-lg transition-all duration-200 ${
        task.completed 
          ? 'bg-gray-50 text-gray-500' 
          : 'bg-white border-gray-100 hover:border-gray-200'
      }`}
    >
      <div className="flex items-center w-full sm:w-auto mb-2 sm:mb-0">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggle(task.id)}
          className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 focus:ring-offset-1 cursor-pointer focus:outline-none focus:ring-2"
          aria-label={task.completed ? `Mark ${task.title} as incomplete` : `Mark ${task.title} as complete`}
        />
        <span
          className={`ml-3 truncate max-w-xs ${task.completed ? 'line-through' : ''}`}
          title={task.title} // Show full title on hover
        >
          {task.title}
        </span>
      </div>
      <button
        onClick={() => onDelete(task.id)}
        className="text-gray-400 hover:text-red-500 px-3 py-1 rounded transition-colors duration-200 w-full sm:w-auto text-center text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        aria-label={`Delete task: ${task.title}`}
      >
        Delete
      </button>
    </div>
  );
};

export default TodoItem;