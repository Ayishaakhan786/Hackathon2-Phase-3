# Tasks: Chat API Foundation

**Input**: Design documents from `/specs/009-chat-api-foundation/`
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

- [X] T001 [P] Update pyproject.toml with required dependencies (SQLModel, asyncpg, Neon PostgreSQL driver)
- [X] T002 [P] Create backend/src/models/conversation.py with Conversation model
- [X] T003 [P] Create backend/src/models/message.py with Message model
- [X] T004 [P] Create backend/src/services/conversation_service.py with service functions
- [X] T005 [P] Create backend/src/services/message_service.py with service functions
- [X] T006 [P] Create backend/src/api/chat_api.py with chat endpoint
- [X] T007 Update backend/src/database/connection.py to include Conversation and Message models

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T008 Configure async database connection with Neon PostgreSQL in backend/src/database/connection.py
- [X] T009 [P] Implement Conversation model with SQLModel in backend/src/models/conversation.py (depends on T002)
- [X] T010 [P] Implement Message model with SQLModel in backend/src/models/message.py (depends on T003)
- [X] T011 [P] Implement create_conversation function in backend/src/services/conversation_service.py (depends on T009)
- [X] T012 [P] Implement get_conversation function in backend/src/services/conversation_service.py (depends on T009)
- [X] T013 [P] Implement save_message function in backend/src/services/message_service.py (depends on T010)
- [X] T014 [P] Implement fetch_conversation_history function in backend/src/services/message_service.py (depends on T010)
- [X] T015 Configure automatic table creation in backend/src/database/connection.py
- [X] T016 Add database dependency injection in backend/src/api/deps.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Start New Chat Conversation (Priority: P1) 🎯 MVP

**Goal**: Enable users to start a new chat conversation by sending a message without a conversation ID, which creates a new conversation and returns the conversation ID with a placeholder response.

**Independent Test**: Can be fully tested by sending a message without a conversation ID and verifying that a new conversation is created, the user message is persisted, a placeholder assistant response is generated, and both messages are accessible in the conversation history.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T017 [P] [US1] Contract test for POST /api/{user_id}/chat endpoint in backend/tests/contract/test_chat_api.py
- [X] T018 [P] [US1] Integration test for new conversation creation in backend/tests/integration/test_new_conversation.py

### Implementation for User Story 1

- [X] T019 [US1] Implement POST /api/{user_id}/chat endpoint in backend/src/api/chat_api.py (depends on T011, T013, T014)
- [X] T020 [US1] Add logic to create new conversation when no conversation_id provided in backend/src/api/chat_api.py (depends on T019)
- [X] T021 [US1] Add logic to save user message to database in backend/src/api/chat_api.py (depends on T019)
- [X] T022 [US1] Add logic to generate placeholder assistant response in backend/src/api/chat_api.py (depends on T019)
- [X] T023 [US1] Add logic to save assistant response to database in backend/src/api/chat_api.py (depends on T019)
- [X] T024 [US1] Return proper response format with conversation_id, response, and empty tool_calls in backend/src/api/chat_api.py (depends on T019)
- [X] T025 [US1] Add validation for incoming message content in backend/src/api/chat_api.py
- [X] T026 [US1] Add error handling for database operations in backend/src/api/chat_api.py
- [X] T027 [US1] Add logging for conversation creation operations in backend/src/api/chat_api.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Continue Existing Chat Conversation (Priority: P1)

**Goal**: Enable users to continue an existing chat conversation by sending a message with a valid conversation ID, appending the message to the existing conversation and returning the assistant's response.

**Independent Test**: Can be fully tested by sending a message with an existing conversation ID and verifying that the message is appended to the conversation history and the assistant's response is returned.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T028 [P] [US2] Contract test for continuing conversation in backend/tests/contract/test_chat_api.py
- [X] T029 [P] [US2] Integration test for continuing existing conversation in backend/tests/integration/test_continue_conversation.py

### Implementation for User Story 2

- [X] T030 [US2] Enhance POST /api/{user_id}/chat endpoint in backend/src/api/chat_api.py to handle existing conversation IDs (depends on T012, T019)
- [X] T031 [US2] Add logic to validate conversation belongs to user in backend/src/api/chat_api.py (depends on T030)
- [X] T032 [US2] Add logic to append user message to existing conversation in backend/src/api/chat_api.py (depends on T030)
- [X] T033 [US2] Add logic to generate and save assistant response for existing conversation in backend/src/api/chat_api.py (depends on T030)
- [X] T034 [US2] Add error handling for invalid conversation IDs in backend/src/api/chat_api.py
- [X] T035 [US2] Add validation to prevent cross-user conversation access in backend/src/api/chat_api.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Access Chat History Across Sessions (Priority: P2)

**Goal**: Enable users to resume their chat conversations after closing and reopening the application, ensuring conversation history remains intact and accessible.

**Independent Test**: Can be fully tested by creating a conversation, storing messages, simulating a session restart, and then retrieving the conversation history to verify persistence.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T036 [P] [US3] Contract test for fetching conversation history in backend/tests/contract/test_chat_api.py
- [X] T037 [P] [US3] Integration test for conversation persistence across sessions in backend/tests/integration/test_conversation_persistence.py

### Implementation for User Story 3

- [X] T038 [P] [US3] Add database indexes for efficient conversation history retrieval in backend/src/models/conversation.py and backend/src/models/message.py
- [X] T039 [US3] Enhance fetch_conversation_history function to return properly formatted messages in backend/src/services/message_service.py (depends on T014)
- [X] T040 [US3] Add caching mechanism for conversation history if needed for performance in backend/src/services/message_service.py
- [X] T041 [US3] Add pagination support for long conversations in backend/src/services/message_service.py
- [X] T042 [US3] Add validation and error handling for conversation history access in backend/src/api/chat_api.py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T043 [P] Update documentation in specs/009-chat-api-foundation/ with implementation details
- [X] T044 Code cleanup and refactoring of backend/src/models/, backend/src/services/, and backend/src/api/
- [X] T045 Performance optimization across all stories
- [X] T046 [P] Additional unit tests in backend/tests/unit/ for models and services
- [X] T047 Security hardening of API endpoints
- [X] T048 Run quickstart.md validation to ensure all functionality works as expected

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
Task: "Contract test for POST /api/{user_id}/chat endpoint in backend/tests/contract/test_chat_api.py"
Task: "Integration test for new conversation creation in backend/tests/integration/test_new_conversation.py"

# Launch all models for User Story 1 together:
Task: "Create Conversation model in backend/src/models/conversation.py"
Task: "Create Message model in backend/src/models/message.py"
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