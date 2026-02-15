# Feature Specification: Core API Development & Business Logic

**Feature Branch**: `004-core-api-tasks`
**Created**: 2026-02-04
**Status**: Draft
**Input**: User description: "Core API Development & Business Logic

Target audience: Backend Developers
Focus: Building RESTful endpoints for Todo operations that enforce user isolation.

Success criteria:
- CRUD Endpoints created: GET /tasks, POST /tasks, PUT /tasks/{id}, DELETE /tasks/{id}.
- All endpoints secured using the Auth Dependency from Spec 2.
- **Strict Data Isolation:** Users can ONLY see/edit their own tasks.
- User ID is automatically extracted from the token (never passed in request body).

Constraints:
- Framework: FastAPI.
- Database: Neon PostgreSQL via SQLModel.
- Response Format: JSON.
- Error Handling: Standard HTTP codes (404 for not found, 401 for unauth).

Not building:
- Frontend UI components.
- Public/Shared task lists."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User scenarios should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - View Personal Task List (Priority: P1)

As an authenticated user, I want to see my personal list of tasks so that I can manage my work effectively.

**Why this priority**: Essential functionality that enables users to view their tasks, forming the basis for all other task operations.

**Independent Test**: Can be fully tested by making an authenticated request to GET /tasks and receiving only tasks associated with the current user.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid token, **When** they request their task list, **Then** they receive only tasks that belong to them
2. **Given** a user is authenticated but has no tasks, **When** they request their task list, **Then** they receive an empty list
3. **Given** a user makes an unauthenticated request, **When** they attempt to access their task list, **Then** they receive a 401 Unauthorized response

---

### User Story 2 - Create New Task (Priority: P1)

As an authenticated user, I want to create new tasks so that I can track my work items.

**Why this priority**: Core functionality that allows users to add tasks, which is fundamental to the todo application.

**Independent Test**: Can be fully tested by making an authenticated POST request to /tasks and successfully creating a task associated with the current user.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid token, **When** they create a new task, **Then** the task is saved with their user ID automatically attached
2. **Given** a user is authenticated, **When** they provide valid task data, **Then** the task is created successfully and returned with all required fields
3. **Given** a user is unauthenticated, **When** they attempt to create a task, **Then** they receive a 401 Unauthorized response

---

### User Story 3 - Update Existing Task (Priority: P2)

As an authenticated user, I want to update my existing tasks so that I can keep them current with my changing needs.

**Why this priority**: Important for task management allowing users to modify task details and completion status.

**Independent Test**: Can be fully tested by making an authenticated PUT request to /tasks/{id} and successfully updating a task that belongs to the current user.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and owns a specific task, **When** they update that task, **Then** the task is updated successfully
2. **Given** a user is authenticated but does not own a specific task, **When** they attempt to update that task, **Then** they receive a 404 Not Found response (as if the task doesn't exist)
3. **Given** a user is unauthenticated, **When** they attempt to update a task, **Then** they receive a 401 Unauthorized response

---

### User Story 4 - Delete Task (Priority: P2)

As an authenticated user, I want to delete tasks I no longer need so that I can keep my task list clean and relevant.

**Why this priority**: Allows users to remove completed or irrelevant tasks, maintaining a clean task list.

**Independent Test**: Can be fully tested by making an authenticated DELETE request to /tasks/{id} and successfully removing a task that belongs to the current user.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and owns a specific task, **When** they delete that task, **Then** the task is removed successfully
2. **Given** a user is authenticated but does not own a specific task, **When** they attempt to delete that task, **Then** they receive a 404 Not Found response (as if the task doesn't exist)
3. **Given** a user is unauthenticated, **When** they attempt to delete a task, **Then** they receive a 401 Unauthorized response

---

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST provide a GET /tasks endpoint that returns only tasks belonging to the authenticated user
- **FR-002**: System MUST provide a POST /tasks endpoint that creates a new task and automatically associates it with the authenticated user
- **FR-003**: System MUST provide a PUT /tasks/{id} endpoint that updates only tasks belonging to the authenticated user
- **FR-004**: System MUST provide a DELETE /tasks/{id} endpoint that deletes only tasks belonging to the authenticated user
- **FR-005**: System MUST enforce authentication on all task endpoints using the Auth Dependency from previous specification
- **FR-006**: System MUST automatically extract User ID from the JWT token (never accept user ID in request body)
- **FR-007**: System MUST implement strict data isolation so users can only access their own tasks
- **FR-008**: System MUST return appropriate HTTP status codes: 200/201 for success, 401 for unauthorized, 404 for not found
- **FR-009**: System MUST return JSON responses for all endpoints
- **FR-010**: System MUST validate task data on creation and updates

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with title, description, completion status, and user association
- **User**: Represents an authenticated user who owns tasks
- **Authentication Token**: Contains user identity information used for access control

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: All CRUD endpoints for tasks are successfully implemented (GET, POST, PUT, DELETE)
- **SC-002**: Authentication is enforced on all task endpoints with proper error handling
- **SC-003**: Data isolation is maintained where users can only access their own tasks
- **SC-004**: User ID is automatically extracted from tokens without being passed in request bodies
- **SC-005**: All endpoints return appropriate HTTP status codes (401, 404) for unauthorized/access-denied scenarios
- **SC-006**: Responses are returned in JSON format as required
- **SC-007**: Task data is properly validated on creation and updates