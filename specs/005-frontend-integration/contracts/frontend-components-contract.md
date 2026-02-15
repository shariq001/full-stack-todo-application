# Frontend Components Contract

## Purpose
This document defines the contract for frontend components that will interact with the backend API for the todo application.

## Components Overview

### 1. Auth Components

#### LoginForm
- **Purpose**: Handle user login functionality
- **Props**:
  - `onLoginSuccess`: Function called when login is successful
  - `onError`: Function called when login fails
- **Events**:
  - `submit`: When user submits login form
  - `change`: When form fields change
- **State**:
  - `email`: User's email input
  - `password`: User's password input
  - `isLoading`: Whether login is in progress
  - `error`: Error message if login fails

#### SignupForm
- **Purpose**: Handle user registration functionality
- **Props**:
  - `onSignupSuccess`: Function called when signup is successful
  - `onError`: Function called when signup fails
- **Events**:
  - `submit`: When user submits signup form
  - `change`: When form fields change
- **State**:
  - `email`: User's email input
  - `password`: User's password input
  - `confirmPassword`: Password confirmation input
  - `isLoading`: Whether signup is in progress
  - `error`: Error message if signup fails

### 2. Todo Components

#### TodoList
- **Purpose**: Display a list of todos for the authenticated user
- **Props**:
  - `todos`: Array of todo items to display
  - `isLoading`: Whether todos are loading
  - `onTodoToggle`: Function called when todo completion status changes
  - `onTodoDelete`: Function called when todo is deleted
- **Events**:
  - `todoToggle`: When a todo's completion status changes
  - `todoDelete`: When a todo is deleted
  - `refresh`: When user requests to refresh the list
- **State**:
  - `filteredTodos`: Todos after applying any filters
  - `isLoading`: Whether the list is loading
  - `error`: Error message if loading fails

#### TodoItem
- **Purpose**: Display a single todo item with interactive controls
- **Props**:
  - `todo`: Todo object to display
  - `onToggle`: Function called when completion status changes
  - `onDelete`: Function called when delete is clicked
  - `onEdit`: Function called when edit is clicked
- **Events**:
  - `toggle`: When completion checkbox is toggled
  - `delete`: When delete button is clicked
  - `edit`: When edit button is clicked
- **State**:
  - `isEditing`: Whether the todo is in edit mode
  - `editText`: Text for editing the todo

#### TodoForm
- **Purpose**: Form for creating and editing todos
- **Props**:
  - `initialData`: Initial data when editing a todo
  - `onSubmit`: Function called when form is submitted
  - `onCancel`: Function called when form is canceled
- **Events**:
  - `submit`: When user submits the form
  - `cancel`: When user cancels the form
  - `change`: When form fields change
- **State**:
  - `title`: Todo title input
  - `description`: Todo description input
  - `isCompleted`: Completion status
  - `error`: Error message if submission fails

### 3. Layout Components

#### ProtectedRoute
- **Purpose**: Wrapper component that protects routes requiring authentication
- **Props**:
  - `children`: Child components to render if authenticated
  - `fallback`: Component to render if not authenticated
  - `redirectPath`: Path to redirect if not authenticated
- **State**:
  - `isAuthenticated`: Whether user is authenticated
  - `isLoading`: Whether authentication status is being checked

#### DashboardLayout
- **Purpose**: Layout wrapper for the dashboard area
- **Props**:
  - `user`: User object for displaying user information
  - `children`: Child components to render inside the layout
- **State**:
  - `sidebarCollapsed`: Whether sidebar is collapsed
  - `mobileMenuOpen`: Whether mobile menu is open

## Data Flow

### Authentication Flow
1. User navigates to protected route
2. ProtectedRoute checks authentication status
3. If not authenticated, redirects to login
4. User fills Login form and submits
5. LoginForm sends credentials to auth service
6. Auth service contacts backend API
7. Backend validates credentials and returns JWT
8. Frontend stores JWT and updates user session
9. Redirects to original route or dashboard

### Todo Management Flow
1. TodoList component mounts and requests todos
2. useTodos hook calls todoService.getTodos()
3. todoService makes API request to GET /tasks
4. Backend returns user's todo list
5. TodoList renders TodoItem components for each todo
6. User interacts with a TodoItem (toggle, edit, delete)
7. TodoItem updates through todoService
8. todoService makes appropriate API request
9. Backend updates todo and returns updated data
10. TodoList updates local state to reflect changes

## API Client Contract

### Methods
- `apiClient.get(endpoint, config)`: Make GET request
- `apiClient.post(endpoint, data, config)`: Make POST request
- `apiClient.put(endpoint, data, config)`: Make PUT request
- `apiClient.delete(endpoint, config)`: Make DELETE request

### Authorization
- All authenticated requests must include `Authorization: Bearer {token}` header
- Token should be automatically refreshed if expired
- Unauthenticated requests should redirect to login

### Error Handling
- Client should handle network errors gracefully
- Server errors should be displayed to user in friendly format
- Failed operations should allow retry

## Loading States
- All API operations should show loading indicators
- Optimistic updates should be used where appropriate
- Error states should be clearly indicated
- Empty states should guide the user on what to do next

## Responsive Design Requirements
- Components should adapt to mobile, tablet, and desktop screens
- Touch-friendly controls for mobile devices
- Appropriate spacing and sizing for each screen size
- Collapsible navigation for smaller screens