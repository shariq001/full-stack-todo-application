---
description: "Task list for CLI Todo App implementation"
---

# Tasks: CLI Todo App

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python 3.13+ project with UV package manager
- [X] T003 [P] Create directory structure: src/models, src/services, src/ui

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create base Task data model in src/models/task.py
- [X] T005 Create TaskManager service in src/services/manager.py
- [X] T006 Create CLI interface structure in src/ui/cli.py
- [X] T007 Create main application entry point in src/main.py
- [X] T008 Configure error handling and validation infrastructure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks to their to-do list with title, description, and initial pending status

**Independent Test**: Can add tasks with titles and descriptions and verify they appear in the list

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Unit test for Task model in tests/unit/test_task.py
- [ ] T010 [P] [US1] Unit test for TaskManager.add_task in tests/unit/test_manager.py

### Implementation for User Story 1

- [X] T011 [P] [US1] Implement Task dataclass in src/models/task.py
- [X] T012 [US1] Implement TaskManager.add_task method in src/services/manager.py
- [X] T013 [US1] Implement CLI menu option for adding tasks in src/ui/cli.py
- [X] T014 [US1] Add input validation for task creation in src/ui/cli.py
- [X] T015 [US1] Add unique ID assignment in src/services/manager.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Enable users to view all tasks in their to-do list with ID, title, description, and status

**Independent Test**: Can add tasks and then view the complete list to verify all tasks appear correctly

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Unit test for TaskManager.get_all_tasks in tests/unit/test_manager.py
- [ ] T017 [P] [US2] Integration test for viewing tasks in tests/integration/test_cli.py

### Implementation for User Story 2

- [X] T018 [P] [US2] Implement TaskManager.get_all_tasks method in src/services/manager.py
- [X] T019 [US2] Implement CLI display functionality in src/ui/cli.py
- [X] T020 [US2] Implement formatted task list rendering in src/ui/cli.py
- [X] T021 [US2] Add empty list handling in src/ui/cli.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Enable users to update the details of existing tasks by ID

**Independent Test**: Can add a task, update its details, and verify the changes persist

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T022 [P] [US3] Unit test for TaskManager.update_task in tests/unit/test_manager.py
- [ ] T023 [P] [US3] Integration test for updating tasks in tests/integration/test_cli.py

### Implementation for User Story 3

- [X] T024 [P] [US3] Implement TaskManager.update_task method in src/services/manager.py
- [X] T025 [US3] Implement CLI menu option for updating tasks in src/ui/cli.py
- [X] T026 [US3] Add ID validation for update operations in src/services/manager.py
- [X] T027 [US3] Add input validation for task updates in src/ui/cli.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Enable users to delete tasks from their to-do list by ID

**Independent Test**: Can add tasks, delete one, and verify it's no longer in the list

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T028 [P] [US4] Unit test for TaskManager.remove_task in tests/unit/test_manager.py
- [ ] T029 [P] [US4] Integration test for deleting tasks in tests/integration/test_cli.py

### Implementation for User Story 4

- [X] T030 [P] [US4] Implement TaskManager.remove_task method in src/services/manager.py
- [X] T031 [US4] Implement CLI menu option for deleting tasks in src/ui/cli.py
- [X] T032 [US4] Add ID validation for delete operations in src/services/manager.py
- [X] T033 [US4] Add confirmation prompt for deletions in src/ui/cli.py

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Enable users to mark tasks as complete or incomplete by ID

**Independent Test**: Can add tasks, mark them as complete/incomplete, and verify status changes

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T034 [P] [US5] Unit test for TaskManager.mark_complete/mark_incomplete in tests/unit/test_manager.py
- [ ] T035 [P] [US5] Integration test for marking tasks in tests/integration/test_cli.py

### Implementation for User Story 5

- [X] T036 [P] [US5] Implement TaskManager.mark_complete method in src/services/manager.py
- [X] T037 [P] [US5] Implement TaskManager.mark_incomplete method in src/services/manager.py
- [X] T038 [US5] Implement CLI menu options for marking tasks in src/ui/cli.py
- [X] T039 [US5] Add ID validation for status change operations in src/services/manager.py

**Checkpoint**: All user stories should now be fully functional together

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T040 [P] Add comprehensive error handling throughout application
- [X] T041 [P] Add user input validation and sanitization
- [X] T042 [P] Improve CLI user experience and menu navigation
- [X] T043 [P] Add graceful shutdown handling in src/main.py
- [X] T044 [P] Add documentation comments to all classes and methods
- [X] T045 Run quickstart validation to ensure all features work together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before UI components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task model in tests/unit/test_task.py"
Task: "Unit test for TaskManager.add_task in tests/unit/test_manager.py"

# Launch all implementation for User Story 1 together:
Task: "Implement Task dataclass in src/models/task.py"
Task: "Implement TaskManager.add_task method in src/services/manager.py"
Task: "Implement CLI menu option for adding tasks in src/ui/cli.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence