---
id: "0006"
title: "spec core api tasks"
stage: spec
date_iso: "2026-02-04"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "core-api-tasks"
branch: "main"
user: "unknown"
command: "/sp.specify"
labels: ["spec", "api", "tasks", "crud", "authentication"]
links:
  spec: "specs/004-core-api-tasks/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/004-core-api-tasks/spec.md"
  - "specs/004-core-api-tasks/checklists/requirements.md"
  - "history/prompts/general/0006-spec-core-api-tasks.general.prompt.md"
tests_yaml:
  - "none"
---

# PHR-0006: spec core api tasks

## Prompt Text

```
Core API Development & Business Logic

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
- Public/Shared task lists.
```

## Response Text

Created a comprehensive specification for the Core API Development & Business Logic, including user scenarios, functional requirements, and success criteria. The specification defines the necessary components for implementing CRUD operations for tasks with strict user isolation and authentication enforcement.

## Outcome Impact

Successfully created the specification document at specs/004-core-api-tasks/spec.md with all required sections. The specification defines the API endpoints for task management with proper authentication and data isolation. Created validation checklist to ensure spec quality.

## Tests Summary

none

## Files Summary

- specs/004-core-api-tasks/spec.md: Main specification document with user scenarios, requirements, and success criteria
- specs/004-core-api-tasks/checklists/requirements.md: Quality checklist for the specification
- history/prompts/general/0006-spec-core-api-tasks.general.prompt.md: PHR document for this work

## Next Prompts

- /sp.plan to create the implementation plan
- /sp.tasks to break down the implementation into actionable tasks

## Reflection Note

The specification successfully captures the requirements for core API development while adhering to the constraints of using FastAPI with SQLModel and enforcing strict user isolation through authentication.

## Failure Modes Observed

None

## Next Experiment to Improve Prompt Quality

None needed - specification completed successfully with all required elements.