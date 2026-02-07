# Todo App Frontend

A responsive todo application built with Next.js 16+, React, and Tailwind CSS, featuring user authentication and secure task management.

## Features

- **User Authentication**: Secure login and signup using Better Auth
- **Todo Management**: Create, read, update, and delete tasks
- **Data Isolation**: Users can only access their own tasks
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Real-time Updates**: Optimistic UI updates for smooth experience
- **Error Handling**: Graceful error handling and loading states

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **UI Library**: React 18+
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth
- **Data Fetching**: Built-in API client with SWR integration
- **Types**: TypeScript

## Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

3. Run the development server:
```bash
npm run dev
```

## Architecture

### Directory Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── login/             # Login page
│   ├── signup/            # Signup page
│   └── dashboard/         # Dashboard pages
├── components/            # React components
│   ├── auth/              # Authentication components
│   ├── layout/            # Layout components
│   └── todo/              # Todo-specific components
├── lib/                   # Utilities and type definitions
├── hooks/                 # Custom React hooks
├── services/              # API services
└── styles/                # Style configurations
```

### Key Components

- **API Client**: Automatically attaches JWT tokens to requests
- **Auth Service**: Integrates with Better Auth for session management
- **Todo Service**: Handles communication with backend API
- **Custom Hooks**: `useAuth` and `useTodos` for state management
- **Protected Routes**: Ensures authentication before accessing dashboard

## API Integration

The frontend communicates with the backend API through a centralized API client that:

- Attaches JWT tokens to all requests automatically
- Handles 401 Unauthorized responses by redirecting to login
- Provides error handling and loading states
- Implements optimistic updates for better UX

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL (e.g., http://localhost:8000)
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Authentication URL (e.g., http://localhost:3000)