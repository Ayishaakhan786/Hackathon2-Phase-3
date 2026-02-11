# Tasks: MCP Server & Task Management Tools

**Input**: Design documents from `/specs/010-mcp-task-tools/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web app structure based on plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Update pyproject.toml with Official MCP SDK dependency
- [X] T002 [P] Create backend/src/models/task.py with Task model
- [X] T003 [P] Create backend/src/services/task_service.py with service functions
- [X] T004 [P] Create backend/src/mcp/server.py with MCP server implementation
- [X] T005 [P] Create backend/src/mcp/tools.py with task tool implementations
- [X] T006 Update backend/src/database/connection.py to include Task model

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T007 Configure async database connection with Neon PostgreSQL in backend/src/db/connection.py
- [X] T008 [P] Implement Task model with SQLModel in backend/src/models/task.py (depends on T002)
- [X] T009 [P] Implement add_task function in backend/src/services/task_service.py (depends on T008)
- [X] T010 [P] Implement list_tasks function in backend/src/services/task_service.py (depends on T008)
- [X] T011 [P] Implement complete_task function in backend/src/services/task_service.py (depends on T008)
- [X] T012 [P] Implement update_task function in backend/src/services/task_service.py (depends on T008)
- [X] T013 [P] Implement delete_task function in backend/src/services/task_service.py (depends on T008)
- [X] T014 Configure automatic table creation in backend/src/db/connection.py
- [X] T015 Initialize MCP server with Official SDK in backend/src/mcp/server.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task via Natural Language (Priority: P1) 🎯 MVP

**Goal**: Enable AI agents to add new tasks using the add_task MCP tool, which creates tasks in the user's personal task list with proper validation and persistence.

**Independent Test**: Can be fully tested by having an AI agent call the add_task MCP tool with a user ID and task details, then verifying that the task appears in the user's task list.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T016 [P] [US1] Contract test for add_task tool in backend/tests/contract/test_mcp_tools.py
- [X] T017 [P] [US1] Integration test for adding new task in backend/tests/integration/test_add_task.py

### Implementation for User Story 1

- [X] T018 [P] [US1] Create Task model in backend/src/models/task.py (depends on T008)
- [X] T019 [US1] Implement add_task function in backend/src/services/task_service.py (depends on T009)
- [X] T020 [US1] Implement add_task MCP tool in backend/src/mcp/tools.py (depends on T019)
- [X] T021 [US1] Add validation for user ownership in add_task tool in backend/src/mcp/tools.py (depends on T020)
- [X] T022 [US1] Add structured JSON response for add_task in backend/src/mcp/tools.py (depends on T020)
- [X] T023 [US1] Add error handling for invalid input in add_task tool in backend/src/mcp/tools.py (depends on T020)
- [X] T024 [US1] Add logging for add_task operations in backend/src/mcp/tools.py (depends on T020)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View and Manage Existing Tasks (Priority: P1)

**Goal**: Enable AI agents to view and manage existing tasks using list_tasks, complete_task, update_task, and delete_task MCP tools with proper validation and persistence.

**Independent Test**: Can be fully tested by having an AI agent call the list_tasks, complete_task, update_task, and delete_task MCP tools and verifying the appropriate changes in the database.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T025 [P] [US2] Contract test for list_tasks tool in backend/tests/contract/test_mcp_tools.py
- [X] T026 [P] [US2] Contract test for complete_task tool in backend/tests/contract/test_mcp_tools.py
- [X] T027 [P] [US2] Contract test for update_task tool in backend/tests/contract/test_mcp_tools.py
- [X] T028 [P] [US2] Contract test for delete_task tool in backend/tests/contract/test_mcp_tools.py
- [X] T029 [P] [US2] Integration test for managing tasks in backend/tests/integration/test_manage_tasks.py

### Implementation for User Story 2

- [X] T030 [P] [US2] Implement list_tasks function in backend/src/services/task_service.py (depends on T010)
- [X] T031 [P] [US2] Implement complete_task function in backend/src/services/task_service.py (depends on T011)
- [X] T032 [P] [US2] Implement update_task function in backend/src/services/task_service.py (depends on T012)
- [X] T033 [P] [US2] Implement delete_task function in backend/src/services/task_service.py (depends on T013)
- [X] T034 [US2] Implement list_tasks MCP tool in backend/src/mcp/tools.py (depends on T030)
- [X] T035 [US2] Implement complete_task MCP tool in backend/src/mcp/tools.py (depends on T031)
- [X] T036 [US2] Implement update_task MCP tool in backend/src/mcp/tools.py (depends on T032)
- [X] T037 [US2] Implement delete_task MCP tool in backend/src/mcp/tools.py (depends on T033)
- [X] T038 [US2] Add validation for user ownership in all management tools in backend/src/mcp/tools.py (depends on T034, T035, T036, T037)
- [X] T039 [US2] Add structured JSON responses for all management tools in backend/src/mcp/tools.py (depends on T034, T035, T036, T037)
- [X] T040 [US2] Add error handling for all management tools in backend/src/mcp/tools.py (depends on T034, T035, T036, T037)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Task Operations (Priority: P2)

**Goal**: Ensure that only authorized users can access and modify their tasks, with proper validation and error handling for unauthorized access attempts.

**Independent Test**: Can be fully tested by attempting to access or modify tasks belonging to different users and verifying that the system properly validates user ownership and rejects unauthorized access.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T041 [P] [US3] Contract test for access validation in backend/tests/contract/test_security.py
- [X] T042 [P] [US3] Integration test for secure task operations in backend/tests/integration/test_security.py

### Implementation for User Story 3

- [X] T043 [P] [US3] Enhance user ownership validation across all tools in backend/src/mcp/tools.py
- [X] T044 [US3] Add comprehensive error responses for unauthorized access in backend/src/mcp/tools.py
- [X] T045 [US3] Add audit logging for access attempts in backend/src/mcp/tools.py
- [X] T046 [US3] Add validation for task existence before operations in backend/src/mcp/tools.py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T047 [P] Update documentation in specs/010-mcp-task-tools/ with implementation details
- [X] T048 Code cleanup and refactoring of backend/src/models/, backend/src/services/, and backend/src/mcp/
- [X] T049 Performance optimization across all stories
- [X] T050 [P] Additional unit tests in backend/tests/unit/ for models and services
- [X] T051 Security hardening of MCP tools
- [X] T052 Run quickstart.md validation to ensure all functionality works as expected

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
Task: "Contract test for add_task tool in backend/tests/contract/test_mcp_tools.py"
Task: "Integration test for adding new task in backend/tests/integration/test_add_task.py"

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