# Quickstart Guide: Frontend Implementation & Integration

**Feature**: Frontend Implementation & Integration
**Date**: 2026-02-02
**Version**: 1.0

## Overview

This guide provides step-by-step instructions to set up the frontend implementation for the todo application, including Next.js UI components, Better Auth integration, and API client configuration for backend communication.

## Prerequisites

- Node.js 18+ and npm/yarn
- Access to the backend API (FastAPI server)
- Better Auth configured in the application
- Git for version control

## Environment Setup

1. **Create the frontend directory structure**:
   ```bash
   mkdir -p frontend/app/{login,signup,dashboard}
   mkdir -p frontend/components/{ui,auth,layout,todo}
   mkdir -p frontend/hooks frontend/lib frontend/services frontend/styles
   ```

2. **Initialize the Next.js project**:
   ```bash
   cd frontend
   npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/lib/*"
   ```

3. **Install additional dependencies**:
   ```bash
   npm install better-auth @better-auth/react swr
   # or
   yarn add better-auth @better-auth/react swr
   ```

4. **Install development dependencies**:
   ```bash
   npm install -D @types/node
   ```

## Configuration Files

### 1. Configure Tailwind CSS

Update `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}
```

### 2. Create Type Definitions

Create `frontend/lib/types.ts`:
```typescript
// User Session Types
export interface UserSession {
  id: string;
  email: string;
  name?: string;
  accessToken: string;
  refreshToken?: string;
  expiresAt: Date;
  isLoggedIn: boolean;
}

// Todo Types
export interface TodoItem {
  id: string;
  title: string;
  description?: string;
  isCompleted: boolean;
  userId: string;
  createdAt: Date;
  updatedAt?: Date;
}

export interface TodoListState {
  todos: TodoItem[];
  isLoading: boolean;
  error: string | null;
  filters?: TodoFilters;
}

export interface TodoFilters {
  status?: 'all' | 'active' | 'completed';
  searchTerm?: string;
}

// Form Types
export interface LoginFormState {
  email: string;
  password: string;
  isLoading: boolean;
  error: string | null;
}

export interface TodoFormState {
  title: string;
  description?: string;
  isLoading: boolean;
  error: string | null;
}

// API Types
export interface ApiClientConfig {
  baseUrl: string;
  headers?: Record<string, string>;
  timeout?: number;
}

export interface ApiErrorResponse {
  error: string;
  message: string;
  statusCode?: number;
}

export interface ValidationError {
  field: string;
  message: string;
}
```

## Implementation Steps

### 1. Create API Client Helper

Create `frontend/lib/api-client.ts`:
```typescript
import { UserSession } from './types';

class ApiClient {
  private baseUrl: string;
  private defaultHeaders: Record<string, string>;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  private async getSessionToken(): Promise<string | null> {
    // Retrieve the session token from wherever it's stored (e.g., context, localStorage)
    // This would typically come from your auth context
    if (typeof window !== 'undefined') {
      const sessionStr = localStorage.getItem('userSession');
      if (sessionStr) {
        const session: UserSession = JSON.parse(sessionStr);
        if (new Date() < new Date(session.expiresAt)) {
          return session.accessToken;
        }
      }
    }
    return null;
  }

  private async buildHeaders(): Promise<Record<string, string>> {
    const headers = { ...this.defaultHeaders };
    const token = await this.getSessionToken();

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = await this.buildHeaders();

    const config: RequestInit = {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `API request failed with status ${response.status}`);
    }

    return response.json();
  }

  async get<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  async post<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }
}

// Create a singleton instance
const apiClient = new ApiClient(process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000');

export default apiClient;
```

### 2. Create Authentication Service

Create `frontend/services/auth-service.ts`:
```typescript
import { UserSession } from '@/lib/types';

class AuthService {
  async getCurrentSession(): Promise<UserSession | null> {
    // Get session from Better Auth
    if (typeof window !== 'undefined') {
      const sessionStr = localStorage.getItem('userSession');
      if (sessionStr) {
        try {
          const sessionData = JSON.parse(sessionStr);
          // Check if session is still valid
          if (new Date() < new Date(sessionData.expiresAt)) {
            return sessionData as UserSession;
          } else {
            // Session expired, remove it
            localStorage.removeItem('userSession');
            return null;
          }
        } catch (error) {
          console.error('Failed to parse session', error);
          localStorage.removeItem('userSession');
          return null;
        }
      }
    }
    return null;
  }

  async setSession(session: UserSession): Promise<void> {
    if (typeof window !== 'undefined') {
      localStorage.setItem('userSession', JSON.stringify(session));
    }
  }

  async clearSession(): Promise<void> {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('userSession');
    }
  }
}

export const authService = new AuthService();
```

### 3. Create Todo Service

Create `frontend/services/todo-service.ts`:
```typescript
import apiClient from '@/lib/api-client';
import { TodoItem } from '@/lib/types';

class TodoService {
  async getTodos(): Promise<TodoItem[]> {
    try {
      const response = await apiClient.get<{ data: TodoItem[] }>('/tasks');
      return response.data.map(todo => ({
        ...todo,
        createdAt: new Date(todo.createdAt),
        updatedAt: todo.updatedAt ? new Date(todo.updatedAt) : undefined,
      }));
    } catch (error) {
      console.error('Failed to fetch todos:', error);
      throw error;
    }
  }

  async createTodo(todo: Omit<TodoItem, 'id' | 'userId' | 'createdAt' | 'updatedAt'>): Promise<TodoItem> {
    try {
      const response = await apiClient.post<{ data: TodoItem }>('/tasks', {
        title: todo.title,
        description: todo.description,
        is_completed: todo.isCompleted || false,
      });

      return {
        ...response.data,
        createdAt: new Date(response.data.createdAt),
        updatedAt: response.data.updatedAt ? new Date(response.data.updatedAt) : undefined,
      };
    } catch (error) {
      console.error('Failed to create todo:', error);
      throw error;
    }
  }

  async updateTodo(id: string, updates: Partial<TodoItem>): Promise<TodoItem> {
    try {
      const response = await apiClient.put<{ data: TodoItem }>(`/tasks/${id}`, {
        title: updates.title,
        description: updates.description,
        is_completed: updates.isCompleted,
      });

      return {
        ...response.data,
        createdAt: new Date(response.data.createdAt),
        updatedAt: response.data.updatedAt ? new Date(response.data.updatedAt) : undefined,
      };
    } catch (error) {
      console.error(`Failed to update todo ${id}:`, error);
      throw error;
    }
  }

  async deleteTodo(id: string): Promise<void> {
    try {
      await apiClient.delete(`/tasks/${id}`);
    } catch (error) {
      console.error(`Failed to delete todo ${id}:`, error);
      throw error;
    }
  }
}

export const todoService = new TodoService();
```

### 4. Create Protected Route Component

Create `frontend/components/auth/protected-route.tsx`:
```typescript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth-service';

interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
}

export default function ProtectedRoute({ children, redirectTo = '/login' }: ProtectedRouteProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      const session = await authService.getCurrentSession();
      setIsAuthenticated(!!session);

      if (!session) {
        router.push(redirectTo);
      }
    };

    checkAuth();
  }, [router, redirectTo]);

  if (isAuthenticated === null) {
    // Loading state while checking authentication
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Render nothing while redirecting
    return null;
  }

  return <>{children}</>;
}
```

### 5. Create Custom Hook for Authentication

Create `frontend/hooks/use-auth.ts`:
```typescript
import { useState, useEffect } from 'react';
import { UserSession } from '@/lib/types';
import { authService } from '@/services/auth-service';

export function useAuth() {
  const [user, setUser] = useState<UserSession | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const session = await authService.getCurrentSession();
        setUser(session);
      } catch (error) {
        console.error('Failed to get session:', error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  const login = async (email: string, password: string) => {
    // This would integrate with Better Auth
    // Placeholder implementation
    setLoading(true);
    try {
      // Call Better Auth login
      // const result = await betterAuth.signIn.email({ email, password });

      // For demo purposes, creating a mock session
      const mockSession: UserSession = {
        id: 'user-123',
        email,
        name: email.split('@')[0],
        accessToken: 'mock-access-token',
        refreshToken: 'mock-refresh-token',
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours from now
        isLoggedIn: true,
      };

      await authService.setSession(mockSession);
      setUser(mockSession);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await authService.clearSession();
      setUser(null);
      // Redirect to login page would happen in the component using this hook
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return { user, loading, login, logout };
}
```

### 6. Create Custom Hook for Todos

Create `frontend/hooks/use-todos.ts`:
```typescript
import { useState, useEffect } from 'react';
import { TodoItem, TodoListState } from '@/lib/types';
import { todoService } from '@/services/todo-service';

export function useTodos() {
  const [state, setState] = useState<TodoListState>({
    todos: [],
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      const todos = await todoService.getTodos();
      setState({ todos, isLoading: false, error: null });
    } catch (error) {
      setState({
        todos: [],
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch todos',
      });
    }
  };

  const createTodo = async (todoData: Omit<TodoItem, 'id' | 'userId' | 'createdAt' | 'updatedAt'>) => {
    try {
      const newTodo = await todoService.createTodo(todoData);
      setState(prev => ({
        ...prev,
        todos: [newTodo, ...prev.todos],
      }));
      return newTodo;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to create todo';
      setState(prev => ({ ...prev, error: errorMessage }));
      throw error;
    }
  };

  const updateTodo = async (id: string, updates: Partial<TodoItem>) => {
    try {
      const updatedTodo = await todoService.updateTodo(id, updates);
      setState(prev => ({
        ...prev,
        todos: prev.todos.map(todo =>
          todo.id === id ? updatedTodo : todo
        ),
      }));
      return updatedTodo;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to update todo';
      setState(prev => ({ ...prev, error: errorMessage }));
      throw error;
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      await todoService.deleteTodo(id);
      setState(prev => ({
        ...prev,
        todos: prev.todos.filter(todo => todo.id !== id),
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete todo';
      setState(prev => ({ ...prev, error: errorMessage }));
      throw error;
    }
  };

  return { ...state, fetchTodos, createTodo, updateTodo, deleteTodo };
}
```

### 7. Update Root Layout

Update `frontend/app/layout.tsx`:
```tsx
import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A simple todo application with authentication',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          {children}
        </Providers>
        </body>
    </html>
  );
}
```

### 8. Create Providers

Create `frontend/app/providers/index.tsx`:
```tsx
'use client';

import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

export function Providers({ children }: Props) {
  return (
    <>
      {children}
    </>
  );
}
```

## Testing the Implementation

### 1. Start the Development Server

```bash
cd frontend
npm run dev
# or
yarn dev
```

### 2. Verify Components

Visit http://localhost:3000 and verify:

1. **Login Flow**:
   - Navigate to `/login` and test the authentication flow
   - Verify protected routes redirect unauthenticated users
   - Test logout functionality

2. **Todo Features**:
   - Access the dashboard at `/dashboard` when authenticated
   - Verify the todo list loads correctly
   - Test creating, updating, and deleting todos
   - Check that changes are reflected immediately in the UI

3. **API Integration**:
   - Verify the API client correctly attaches JWT tokens
   - Check error handling when the backend is unavailable
   - Verify loading states during API operations

## Key Components

### Core Components
- `frontend/lib/api-client.ts` - API client utility with automatic JWT token attachment
- `frontend/services/auth-service.ts` - Authentication management service
- `frontend/services/todo-service.ts` - Todo API service
- `frontend/components/auth/protected-route.tsx` - Route protection component
- `frontend/hooks/use-auth.ts` - Authentication hook
- `frontend/hooks/use-todos.ts` - Todo management hook

### UI Components
- Authentication forms (login, signup)
- Todo list and item components
- Loading and error state components
- Navigation and layout components

## Verification Commands

### 1. Check API Client Functionality

```bash
# Verify the API client is properly configured
npm run build
# Should build successfully without errors
```

### 2. Test Authentication Flow

1. Access a protected route (e.g., `/dashboard`) without being logged in
2. Should be redirected to `/login`
3. After successful login, should be redirected back to the intended page

### 3. Test Todo Operations

1. Create a new todo and verify it appears in the list immediately
2. Update a todo and verify changes are reflected in the UI
3. Delete a todo and verify it's removed from the list
4. Refresh the page and verify todos are persisted from the backend

## Troubleshooting

### Common Issues

1. **API Token Not Attached**:
   - Verify `apiClient` retrieves session token correctly
   - Check that authentication state is properly stored and retrieved
   - Confirm the Authorization header format is `Bearer <token>`

2. **Protected Route Not Working**:
   - Verify `ProtectedRoute` component is properly wrapping protected pages
   - Check that `authService` correctly detects session status
   - Ensure redirects are happening as expected

3. **Todo Operations Not Updating UI**:
   - Confirm `use-todos` hook is properly updating state
   - Check for race conditions in async operations
   - Verify optimistic updates are working correctly

### Verification Commands

```bash
# Test that the app builds without errors
npm run build

# Run type checking
npx tsc --noEmit

# Test a basic end-to-end flow
# 1. Navigate to home page (should redirect to login if not authenticated)
# 2. Login with valid credentials
# 3. Create a new task
# 4. Verify the task appears in the list
# 5. Logout and verify session is cleared
```

## Next Steps

1. Implement proper Better Auth integration (replacing the mock implementation)
2. Add form validation and error handling
3. Enhance UI with better loading states and error displays
4. Add more sophisticated filtering and sorting options for todos
5. Implement offline support using service workers
6. Add comprehensive error boundaries and logging
7. Set up automated testing (unit and end-to-end)

## Security Notes

- JWT tokens should be stored securely, preferably in httpOnly cookies when possible
- Implement proper input sanitization for all user inputs
- Add rate limiting on the frontend to prevent API abuse
- Validate all data received from the API before using it
- Ensure all routes that require authentication are properly protected