# Implementation Plan: Core API Development & Business Logic

**Branch**: `004-core-api-tasks` | **Date**: 2026-02-04 | **Spec**: [specs/004-core-api-tasks/spec.md](specs/004-core-api-tasks/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of core API endpoints for task management with strict user isolation enforced through authentication dependency injection and SQLModel query filtering. The architecture ensures that users can only access and modify their own tasks through automatic user ID extraction from JWT tokens and secure data access patterns.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.10+
**Primary Dependencies**: FastAPI, SQLModel, Pydantic, python-jose
**Storage**: Neon PostgreSQL
**Testing**: pytest with unit and integration tests
**Target Platform**: Linux server (Cloud deployment ready)
**Project Type**: Backend API service
**Performance Goals**: <200ms average response time for CRUD operations, efficient query execution
**Constraints**: <200ms p95 CRUD response time, strict data isolation between users, no unauthorized access
**Scale/Scope**: Support initial 10k users with efficient filtering, scalable query patterns

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Agentic Workflow: Follow "Spec → Plan → Task → Implement" cycle as per constitution
- User Isolation: Enforce strict data isolation through user_id filtering in all queries
- Stateless Architecture: Use JWT-based authentication without server-side sessions
- Persistence: Proper SQLModel integration with Neon PostgreSQL for reliable data storage
- Clean Architecture: Clear separation between API routes, business logic, and data models
- Reliability: Proper error handling for authentication and data access failures
- Maintainability: Follow PEP 8 standards with type hints and clean code practices

## API Endpoint Specifications

### GET /tasks
- **Purpose**: Retrieve all tasks belonging to the authenticated user
- **Authentication**: Required via `current_user` dependency
- **Query**: `SELECT * FROM tasks WHERE user_id = :current_user_id`
- **Response**: List of task objects in JSON format
- **Status Codes**: 200 (success), 401 (unauthorized)

### POST /tasks
- **Purpose**: Create a new task for the authenticated user
- **Authentication**: Required via `current_user` dependency
- **Logic**: Attach current_user.id to new task record
- **Response**: Created task object in JSON format
- **Status Codes**: 201 (created), 401 (unauthorized), 422 (validation error)

### PUT /tasks/{id}
- **Purpose**: Update an existing task owned by the authenticated user
- **Authentication**: Required via `current_user` dependency
- **Query**: `SELECT * FROM tasks WHERE id = :task_id AND user_id = :current_user_id`
- **Validation**: Task must exist and be owned by current user
- **Response**: Updated task object in JSON format
- **Status Codes**: 200 (success), 401 (unauthorized), 404 (not found), 422 (validation error)

### DELETE /tasks/{id}
- **Purpose**: Delete an existing task owned by the authenticated user
- **Authentication**: Required via `current_user` dependency
- **Query**: `DELETE FROM tasks WHERE id = :task_id AND user_id = :current_user_id`
- **Validation**: Task must exist and be owned by current user
- **Response**: Empty response with success status
- **Status Codes**: 204 (deleted), 401 (unauthorized), 404 (not found)

## Project Structure

### Documentation (this feature)

```text
specs/004-core-api-tasks/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command output)
├── data-model.md        # Phase 1 output (/sp.plan command output)
├── quickstart.md        # Phase 1 output (/sp.plan command output)
├── contracts/           # Phase 1 output (/sp.plan command output)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py      # User model (from previous spec)
│   │   ├── task.py      # Task model with Pydantic response schemas
│   │   └── base.py      # Base SQLModel class (from previous spec)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── database.py  # Database connection management (from previous spec)
│   │   ├── auth.py      # Authentication service (from previous spec)
│   │   └── task_service.py # Business logic for task operations
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py      # FastAPI app instance (from previous spec)
│   │   ├── tasks.py     # Task CRUD endpoints with authentication
│   │   ├── health.py    # Health check endpoint (from previous spec)
│   │   └── deps.py      # Dependency injection including current_user
│   └── main.py          # Application entry point (from previous spec)
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Pytest configuration
│   ├── test_health.py   # Health check endpoint tests (from previous spec)
│   ├── test_tasks.py    # Task endpoint tests with isolation verification
│   ├── test_auth.py     # Authentication tests (from previous spec)
│   └── test_database.py # Database connection tests (from previous spec)
├── requirements.txt
├── .env.example         # Example environment variables file
└── .env                 # Local environment variables (gitignored)
```

**Structure Decision**: Backend API service extending the existing structure with new task endpoints and services. Maintains clear separation between models, services, and API layers for clean architecture compliance.

## Key Design Decisions

1. **Data Isolation Strategy**:
   - Inject `current_user` dependency into every route handler
   - Filter queries using: `select(Task).where(Task.user_id == current_user.id)`
   - Prevent direct access to tasks not owned by current user

2. **Response Models vs DB Models**:
   - Use separate Pydantic models for API responses to exclude sensitive fields
   - Database models contain all fields including foreign keys
   - Response models exclude password hashes, internal IDs, and other sensitive data

3. **Partial Updates Handling**:
   - Use PUT for full updates (replace entire resource)
   - Consider PATCH for future implementation of partial updates
   - Current implementation focuses on PUT for consistency

4. **Phased Implementation Strategy**:
   - Phase 1: Route Definition → Define all four CRUD endpoints with authentication
   - Phase 2: Controller Logic → Implement business logic for each endpoint
   - Phase 3: Data Isolation Check → Ensure strict filtering and validation
   - Phase 4: Swagger Verification → Verify API documentation and test endpoints

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |