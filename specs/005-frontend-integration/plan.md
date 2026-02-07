# Implementation Plan: Frontend Implementation & Integration

**Branch**: `005-frontend-integration` | **Date**: 2026-02-04 | **Spec**: [specs/005-frontend-integration/spec.md](specs/005-frontend-integration/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a responsive Next.js frontend with Better Auth integration for user authentication, API client wrapper for backend communication, and a complete todo management interface with protected routes. The architecture follows Next.js App Router patterns with Tailwind CSS styling and React Hook state management.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: TypeScript (Next.js 16+), JavaScript/TypeScript for React components
**Primary Dependencies**: Next.js 16+, React 18+, Better Auth, Tailwind CSS, SWR/react-query for data fetching
**Storage**: Browser local storage, Better Auth session management
**Testing**: Playwright for end-to-end testing, Jest/React Testing Library for unit tests
**Target Platform**: Web browsers (Responsive design for mobile, tablet, desktop)
**Project Type**: Web application (Frontend)
**Performance Goals**: <100ms page load times, smooth UI interactions, efficient data fetching
**Constraints**: <200ms p95 page response time, proper loading states, responsive design compliance
**Scale/Scope**: Support initial 10k users with optimized client-side performance

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Agentic Workflow: Follow "Spec → Plan → Task → Implement" cycle as per constitution
- User Isolation: Ensure frontend only accesses data for the authenticated user
- Stateless Architecture: Use JWT-based authentication from backend without server-side sessions
- Persistence: Properly manage client-side state and sync with backend as needed
- Clean Architecture: Clear separation between UI components, data fetching, and business logic
- Reliability: Proper error handling for API failures and authentication issues
- Maintainability: Follow React/Next.js best practices with TypeScript and Tailwind CSS

## Wireframes & UI Layout

### Dashboard Layout
```
┌─────────────────────────────────────────┐
│ Header                                │
│ ┌─Logo──┐ ┌Nav Menu┐ ┌User Profile┐   │
├─────────────────────────────────────────┤
│ Sidebar        │ Main Content Area    │
│ ┌─────────────┐│ ┌──────────────────┐ │
│ │- Dashboard │││ │   Todo List      │ │
│ │- My Tasks  │││ │                  │ │
│ │- Settings  │││ │ [Add New Task]   │ │
│ └─────────────┘││ │                  │ │
│               ││ │ [Task Items...]  │ │
│               ││ │                  │ │
│               ││ └──────────────────┘ │
└─────────────────────────────────────────┘
```

### Login Page Layout
```
┌─────────────────────────────────────────┐
│                                       │
│              Login                    │
│                                       │
│  ┌─────────────────────────────────┐  │
│  │                                 │  │
│  │  Welcome Back                   │  │
│  │                                 │  │
│  │  Email: [________________]      │  │
│  │                                 │  │
│  │  Password: [_______________]    │  │
│  │                                 │  │
│  │  [Sign In]   [Forgot Password?] │  │
│  │                                 │  │
│  │  Don't have an account?         │  │
│  │  [Sign Up]                      │  │
│  │                                 │  │
│  └─────────────────────────────────┘  │
│                                       │
└─────────────────────────────────────────┘
```

## Project Structure

### Documentation (this feature)

```text
specs/005-frontend-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── layout.tsx           # Root layout with global styles
│   ├── page.tsx             # Home page (redirects to dashboard if authenticated)
│   ├── login/
│   │   └── page.tsx         # Login page
│   ├── signup/
│   │   └── page.tsx         # Signup page
│   ├── dashboard/
│   │   ├── page.tsx         # Main dashboard page
│   │   └── layout.tsx       # Dashboard-specific layout
│   ├── globals.css          # Global styles and Tailwind imports
│   └── providers/           # Context providers (auth, theme, etc.)
│       └── auth-provider.tsx
├── components/
│   ├── ui/                  # Reusable UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── ...
│   ├── auth/                # Authentication components
│   │   ├── login-form.tsx
│   │   ├── signup-form.tsx
│   │   └── protected-route.tsx
│   ├── layout/              # Layout components
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   └── navigation.tsx
│   └── todo/                # Todo-specific components
│       ├── todo-list.tsx
│       ├── todo-item.tsx
│       ├── todo-form.tsx
│       └── todo-filters.tsx
├── lib/
│   ├── api-client.ts        # API client utility wrapper
│   ├── auth-utils.ts        # Authentication utilities
│   ├── types.ts             # TypeScript type definitions
│   └── constants.ts         # Application constants
├── hooks/
│   ├── use-auth.ts          # Authentication hook
│   ├── use-todos.ts         # Todo management hook
│   └── ...
├── services/
│   ├── auth-service.ts      # Better Auth integration service
│   └── todo-service.ts      # Todo API service
├── styles/
│   └── tailwind.config.js   # Tailwind CSS configuration
├── public/
│   └── ...
├── package.json
├── tsconfig.json
└── next.config.js
```

**Structure Decision**: Frontend application following Next.js App Router conventions with clear separation of concerns between UI components, data fetching services, and business logic. Authentication and data management are encapsulated in dedicated services and hooks.

## Key Design Decisions

1. **Client-side vs Server-side Fetching Strategy**:
   - Use client-side fetching with SWR for dynamic todo data
   - Server-side rendering for initial page loads where SEO is important
   - Cache-first strategy for better user experience
   - Optimistic updates for immediate UI feedback

2. **Loading State UI**:
   - Skeleton screens during initial data loading
   - Progress indicators for API operations
   - Error boundaries for graceful error handling
   - Optimistic UI updates for create/edit/delete actions

3. **API Client Helper Implementation**:
   - Create centralized `apiClient` utility
   - Automatically retrieve and attach JWT token to requests
   - Handle token expiration and refresh
   - Implement error handling and retry logic

4. **Protected Routes Strategy**:
   - Higher-order component for route protection
   - Redirect to login if no valid session
   - Check authentication status on protected route access
   - Persist user's intended destination for post-login redirect

5. **Phased Implementation Strategy**:
   - Phase 1: UI Layout → Create responsive layout components and styling
   - Phase 2: Auth Integration → Integrate Better Auth for login/signup functionality
   - Phase 3: API Wiring → Connect frontend to backend API endpoints
   - Phase 4: State Management → Implement React Hook-based state management

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |