---
id: 007
title: Core-Todo-API-Implementation
stage: tasks
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: core-api-tasks
branch: main
user: Muhammad Shariq
command: /sp.implement
labels: ["api", "todo", "crud", "authentication", "data-isolation", "fastapi"]
links:
  spec: specs/004-core-api-tasks/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/api/tasks.py
  - backend/src/schemas/task_schemas.py
  - backend/src/services/task_service.py
  - backend/src/services/database.py
  - backend/src/models/task.py
  - backend/src/main.py
  - specs/004-core-api-tasks/tasks.md
  - verify_api.py
tests:
  - verify_api.py
---

## Prompt

/implement

Context Files:
- sp.constitution
- sp.specify.3.core_api.md
- sp.plan.3.core_api.md
- sp.tasks.3.core_api.md

Instruction:
You are the Senior Backend Developer. Your goal is to build the Core Todo API with strict data isolation.

Directives:
1. Create the Pydantic schemas and API Routers for Tasks.
2. Inject the `get_current_user` dependency (from Spec 2) into ALL task routes.
3. CRITICAL: Ensure every database query filters by `user_id`. Users must NEVER see other users' data.
4. strictly follow the "sp.tasks.3.core_api.md" checklist.

Execute step-by-step. After implementing, verify that a user cannot access a task ID belonging to another user.

## Response snapshot

Successfully implemented the complete Core Todo API with strict data isolation. The implementation includes:

✅ Pydantic schemas for TaskCreate, TaskRead, and TaskUpdate models
✅ FastAPI routers for complete CRUD operations (GET, POST, PUT, DELETE)
✅ Authentication dependency injection with `get_current_user` in all endpoints
✅ Strict data isolation through user_id filtering in all database queries
✅ Task service layer with proper business logic and ownership verification
✅ Database session dependency injection for FastAPI
✅ Complete CRUD endpoints with proper HTTP status codes
✅ Verification script confirming all functionality works correctly

The API enforces strict data isolation ensuring users can only access their own tasks, with proper error handling for unauthorized access attempts.

## Outcome

- ✅ Impact: Complete Core Todo API with full CRUD and strict data isolation implemented
- 🧪 Tests: All API components verified with 100% success rate
- 📁 Files: 8 critical files updated/created for complete API functionality
- 🔁 Next prompts: Ready for frontend integration and user interface development
- 🧠 Reflection: Clean separation of concerns maintained between models, services, and API layers

## Evaluation notes (flywheel)

- Failure modes observed: None - all components working as expected
- Graders run and results (PASS/FAIL): PASS - 100% verification success rate
- Prompt variant (if applicable): Standard implementation workflow
- Next experiment (smallest change to try): Frontend integration with API endpoints