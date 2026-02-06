# Tasks: Backend API & Database

**Input**: Design documents from `/specs/002-backend-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan with backend/src/{models,services,api,core} directories
- [X] T002 [P] Initialize Python project with FastAPI, SQLModel, and Neon PostgreSQL dependencies in backend/
- [X] T003 [P] Configure linting and formatting tools for backend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Setup database schema and migrations framework in backend/src/database.py
- [X] T005 [P] Implement authentication/authorization framework in backend/src/core/security.py
- [X] T006 [P] Setup API routing and middleware structure in backend/src/main.py
- [X] T007 Create base models/entities that all stories depend on in backend/src/models/base.py
- [X] T008 Configure error handling and logging infrastructure in backend/src/core/config.py
- [X] T009 Setup environment configuration management in backend/src/core/config.py
- [X] T010 [P] Create authentication dependency in backend/src/api/deps.py
- [X] T011 [P] Import existing User model from Spec 1 in backend/src/models/user.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create a Task (Priority: P1) 🎯 MVP

**Goal**: Allow authenticated users to create new tasks in their personal task list

**Independent Test**: Can be fully tested by authenticating as a user, calling the POST /api/{user_id}/tasks endpoint with valid task data, and verifying that the task is created and returned with a unique ID.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US1] Contract test for POST /api/{user_id}/tasks in backend/tests/contract/test_tasks.py
- [ ] T013 [P] [US1] Unit test for Task model validation in backend/tests/unit/test_task_model.py

### Implementation for User Story 1

- [X] T014 [P] [US1] Create Task model in backend/src/models/task.py
- [X] T015 [US1] Implement TaskService for task creation in backend/src/services/task_service.py
- [X] T016 [US1] Implement create task endpoint in backend/src/api/tasks.py
- [X] T017 [US1] Add validation and error handling for task creation in backend/src/api/tasks.py
- [X] T018 [US1] Add authorization check to ensure user can only create tasks for themselves in backend/src/api/tasks.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View User's Tasks (Priority: P1)

**Goal**: Allow authenticated users to view all their tasks in a list

**Independent Test**: Can be fully tested by authenticating as a user, creating some tasks, calling the GET /api/{user_id}/tasks endpoint, and verifying that only that user's tasks are returned.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Contract test for GET /api/{user_id}/tasks in backend/tests/contract/test_tasks.py
- [ ] T020 [P] [US2] Integration test for user task isolation in backend/tests/integration/test_task_isolation.py

### Implementation for User Story 2

- [X] T021 [P] [US2] Implement TaskService method to get user's tasks in backend/src/services/task_service.py
- [X] T022 [US2] Implement get user's tasks endpoint in backend/src/api/tasks.py
- [X] T023 [US2] Add authorization check to ensure user can only view their own tasks in backend/src/api/tasks.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update and Manage Tasks (Priority: P2)

**Goal**: Allow authenticated users to update, complete, or delete their tasks

**Independent Test**: Can be tested by authenticating as a user, performing various operations (PUT, PATCH, DELETE) on their own tasks, and verifying that operations succeed while operations on other users' tasks fail.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] Contract test for PUT /api/{user_id}/tasks/{id} in backend/tests/contract/test_tasks.py
- [ ] T025 [P] [US3] Contract test for PATCH /api/{user_id}/tasks/{id}/complete in backend/tests/contract/test_tasks.py
- [ ] T026 [P] [US3] Contract test for DELETE /api/{user_id}/tasks/{id} in backend/tests/contract/test_tasks.py
- [ ] T027 [P] [US3] Integration test for task management operations in backend/tests/integration/test_task_management.py

### Implementation for User Story 3

- [X] T028 [P] [US3] Implement TaskService methods for update, delete, and toggle completion in backend/src/services/task_service.py
- [X] T029 [US3] Implement get task by ID endpoint in backend/src/api/tasks.py
- [X] T030 [US3] Implement update task endpoint in backend/src/api/tasks.py
- [X] T031 [US3] Implement delete task endpoint in backend/src/api/tasks.py
- [X] T032 [US3] Implement toggle task completion endpoint in backend/src/api/tasks.py
- [X] T033 [US3] Add authorization checks to ensure user can only manage their own tasks in backend/src/api/tasks.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T034 [P] Documentation updates in docs/
- [ ] T035 Code cleanup and refactoring
- [ ] T036 Performance optimization across all stories
- [ ] T037 [P] Additional unit tests (if requested) in backend/tests/unit/
- [ ] T038 Security hardening
- [ ] T039 Run quickstart.md validation

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
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
Task: "Contract test for POST /api/{user_id}/tasks in backend/tests/contract/test_tasks.py"
Task: "Unit test for Task model validation in backend/tests/unit/test_task_model.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend/src/models/task.py"
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
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
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