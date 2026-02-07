'use client';

import TodoList from '@/components/todo/todo-list';
import TodoForm from '@/components/todo/todo-form';
import { useTodos } from '@/hooks/use-todos';

export default function DashboardPage() {
  const { createTodo } = useTodos();

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">My Tasks</h1>
          <p className="text-gray-600">Here&apos;s what you need to do today. Stay productive!</p>
        </div>

        <div className="mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Create New Task</h2>
            <TodoForm onSubmit={createTodo} />
          </div>
        </div>

        <div>
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-lg font-semibold text-gray-800">Your Tasks</h2>
              <span className="bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded-full">
                All tasks
              </span>
            </div>
            <TodoList />
          </div>
        </div>
      </div>
    </div>
  );
}
