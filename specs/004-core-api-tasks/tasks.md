# Implementation Tasks: Core API Development & Business Logic

**Feature**: Core API Development & Business Logic
**Branch**: `004-core-api-tasks`
**Date**: 2026-02-04
**Spec**: [specs/004-core-api-tasks/spec.md](specs/004-core-api-tasks/spec.md)
**Plan**: [specs/004-core-api-tasks/plan.md](specs/004-core-api-tasks/plan.md)

## Implementation Strategy

Build the Task CRUD API in iterative phases focusing on the Controller/Router layer, with strict attention to data isolation. Each endpoint should include the user_id filter in all database operations. The implementation follows a phased approach from route definition to data isolation verification.

**MVP Scope**: User Story 1 (View Personal Task List) and User Story 2 (Create New Task) to create a functional, testable API.

## Dependencies

- User Story 3 (Update Existing Task) and User Story 4 (Delete Task) require User Story 2 (Create New Task) to have test data
- Authentication dependency from previous feature (Spec 2) must be available

## Parallel Execution Opportunities

Within the implementation, some tasks can be executed in parallel:
- Schemas can be created in parallel with the router
- Different endpoints can be implemented in parallel after the basic router structure is in place

## Phase 1: Schema Definitions

- [X] T001 Create schemas directory in backend/src/ if it doesn't exist
- [X] T002 Create `backend/src/schemas/task_schemas.py` for Pydantic models
- [X] T003 Define TaskCreate Pydantic model in task_schemas.py with required fields
- [X] T004 Define TaskRead Pydantic model in task_schemas.py with all fields including ID
- [X] T005 Define TaskUpdate Pydantic model in task_schemas.py with optional fields
- [X] T006 Add proper validation rules to all task schemas
- [X] T007 Import and export all task schemas in task_schemas.py __init__ section

## Phase 2: Router Setup

- [X] T008 Create `backend/src/api/tasks.py` router file
- [X] T009 Set up FastAPI router instance for task endpoints
- [X] T010 Import required dependencies (FastAPI, APIRouter, Depends, HTTPException)
- [X] T011 Import authentication dependency from auth module
- [X] T012 Import task schemas from schemas module
- [X] T013 Import database session dependency
- [X] T014 Import task service module (to be created)

## Phase 3: Task Service Layer

- [X] T015 Create `backend/src/services/task_service.py` for business logic
- [X] T016 Define function to get tasks by user_id with proper filtering
- [X] T017 Define function to create task with user_id association
- [X] T018 Define function to get task by ID and user_id (ownership verification)
- [X] T019 Define function to update task with ownership verification
- [X] T020 Define function to delete task with ownership verification
- [X] T021 Add proper error handling and return types to all functions

## Phase 4: User Story 1 - View Personal Task List (Priority: P1)

**Goal**: Allow authenticated users to see their personal list of tasks to manage their work effectively.

**Independent Test Criteria**: Making an authenticated request to GET /tasks and receiving only tasks associated with the current user.

- [X] T022 Implement `GET /tasks` endpoint in the task router
- [X] T023 Inject authentication dependency to get current user
- [X] T024 Call task service to get tasks filtered by current user's ID
- [X] T025 Return task list with proper response model (TaskRead[])
- [X] T026 Ensure response includes only tasks belonging to authenticated user
- [X] T027 Add proper HTTP status codes (200 for success, 401 for unauthorized)
- [X] T028 Test endpoint to verify it returns only user's own tasks

## Phase 5: User Story 2 - Create New Task (Priority: P1)

**Goal**: Allow authenticated users to create new tasks to track their work items.

**Independent Test Criteria**: Making an authenticated POST request to /tasks and successfully creating a task associated with the current user.

- [X] T029 Implement `POST /tasks` endpoint in the task router
- [X] T030 Inject authentication dependency to get current user
- [X] T031 Accept TaskCreate model in request body
- [X] T032 Call task service to create task with current user's ID
- [X] T033 Return created task with proper response model (TaskRead)
- [X] T034 Set HTTP status code to 201 Created
- [X] T035 Ensure user ID is automatically attached from token (not request body)
- [X] T036 Test endpoint to verify task is created with proper user association

## Phase 6: User Story 3 - Update Existing Task (Priority: P2)

**Goal**: Allow authenticated users to update their existing tasks to keep them current with changing needs.

**Independent Test Criteria**: Making an authenticated PUT request to /tasks/{id} and successfully updating a task that belongs to the current user.

- [X] T037 Implement `PUT /tasks/{id}` endpoint in the task router
- [X] T038 Inject authentication dependency to get current user
- [X] T039 Accept task_id as path parameter
- [X] T040 Accept TaskUpdate model in request body
- [X] T041 Verify task ownership by checking user_id filter (return 404 if not owned)
- [X] T042 Call task service to update task with ownership verification
- [X] T043 Return updated task with proper response model (TaskRead)
- [X] T044 Set HTTP status code to 200 OK
- [X] T045 Test endpoint to verify updates only occur for owned tasks

## Phase 7: User Story 4 - Delete Task (Priority: P2)

**Goal**: Allow authenticated users to delete tasks they no longer need to keep their task list clean and relevant.

**Independent Test Criteria**: Making an authenticated DELETE request to /tasks/{id} and successfully removing a task that belongs to the current user.

- [X] T046 Implement `DELETE /tasks/{id}` endpoint in the task router
- [X] T047 Inject authentication dependency to get current user
- [X] T048 Accept task_id as path parameter
- [X] T049 Verify task ownership by checking user_id filter (return 404 if not owned)
- [X] T050 Call task service to delete task with ownership verification
- [X] T051 Set HTTP status code to 204 No Content
- [X] T052 Test endpoint to verify only owned tasks can be deleted

## Phase 8: Router Registration & Integration

- [X] T053 Register the task router in `backend/src/api/main.py`
- [X] T054 Update main application to include task routes
- [X] T055 Ensure all task endpoints are properly mounted
- [X] T056 Verify router prefix and tags are properly set

## Phase 9: Data Isolation Verification

- [X] T057 Test that users cannot access tasks belonging to other users
- [X] T058 Verify all DB operations include user_id filter in queries
- [X] T059 Test that update/delete operations verify ownership before proceeding
- [X] T060 Confirm 404 responses when accessing non-owned tasks (not 403)
- [X] T061 Test error handling for invalid requests and authentication failures

## Phase 10: Testing & Verification

- [X] T062 Create unit tests for each task endpoint in backend/tests/test_tasks.py
- [X] T063 Write integration tests for user isolation verification
- [X] T064 Create test to verify user A cannot access user B's data
- [X] T065 Test all HTTP status codes (401, 404, 200, 201, 204) work correctly
- [X] T066 Run all tests to ensure endpoints work as expected
- [X] T067 Create Swagger UI manual test plan to validate API documentation
- [X] T068 Verify all endpoints appear correctly in API documentation
- [X] T069 Document the task API endpoints and usage
- [X] T070 Run verify_api.py script to confirm all CRUD operations work correctly