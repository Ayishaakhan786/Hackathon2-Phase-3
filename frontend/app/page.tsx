"use client";

import { useState } from 'react';
import TodoItem from './components/todo-item';
import ClientWrapper from './client-wrapper';

// Define TypeScript interfaces
export interface Task {
  id: string;
  title: string;
  completed: boolean;
  createdAt: Date;
}

export interface TaskList {
  tasks: Task[];
  filter?: string; // for potential future use
}

const TodoPage = () => {
  // Initialize with some example tasks
  const [tasks, setTasks] = useState<Task[]>([
    { id: '1', title: 'Learn Next.js', completed: true, createdAt: new Date() },
    { id: '2', title: 'Build a todo app', completed: false, createdAt: new Date() },
    { id: '3', title: 'Deploy to production', completed: false, createdAt: new Date() },
  ]);

  const [newTaskTitle, setNewTaskTitle] = useState('');

  const handleAddTask = () => {
    if (newTaskTitle.trim() !== '') {
      const newTask: Task = {
        id: Date.now().toString(),
        title: newTaskTitle.trim(),
        completed: false,
        createdAt: new Date(),
      };
      setTasks([...tasks, newTask]);
      setNewTaskTitle(''); // Clear the input field
    }
  };

  const handleToggleTask = (id: string) => {
    setTasks(
      tasks.map((task) =>
        task.id === id ? { ...task, completed: !task.completed } : task
      )
    );
  };

  const handleDeleteTask = (id: string) => {
    setTasks(tasks.filter((task) => task.id !== id));
  };

  return (
    <ClientWrapper>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8 px-4">
        <div className="max-w-md mx-auto bg-white rounded-xl shadow-sm overflow-hidden md:max-w-2xl">
          <div className="p-4 sm:p-6">
            <h1 className="text-2xl font-semibold text-center text-gray-800 mb-6">Todo App</h1>

            {/* Task Input Section */}
            <div className="flex flex-col sm:flex-row gap-2 mb-6">
              <input
                type="text"
                value={newTaskTitle}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                placeholder="Enter a new task..."
                className="flex-grow px-4 py-3 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-800 focus:border-gray-800 transition-all duration-200 text-gray-900"
                onKeyDown={(e) => e.key === 'Enter' && handleAddTask()}
                aria-label="Enter a new task"
              />
              <button
                onClick={handleAddTask}
                className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-lg transition duration-200 font-medium shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                aria-label="Add new task"
              >
                Add Task
              </button>
            </div>

            {/* Task List Section */}
            <div className="space-y-2">
              {tasks.map((task) => (
                <TodoItem
                  key={task.id}
                  task={task}
                  onToggle={handleToggleTask}
                  onDelete={handleDeleteTask}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </ClientWrapper>
  );
};

export default TodoPage;