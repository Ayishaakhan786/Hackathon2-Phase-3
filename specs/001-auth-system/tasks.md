# Tasks: Authentication & User Foundation

**Input**: Design documents from `/specs/001-auth-system/`
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

- [X] T001 Create project structure per implementation plan with backend/ and frontend/ directories
- [X] T002 [P] Initialize Python project with FastAPI, SQLModel, and Neon PostgreSQL dependencies in backend/
- [X] T003 [P] Initialize Next.js 16+ project with Better Auth dependencies in frontend/
- [X] T004 [P] Configure linting and formatting tools for both backend and frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T005 Setup database schema and migrations framework in backend/src/database.py
- [X] T006 [P] Implement authentication/authorization framework in backend/src/core/security.py
- [X] T007 [P] Setup API routing and middleware structure in backend/src/main.py
- [X] T008 Create base models/entities that all stories depend on in backend/src/models/base.py
- [X] T009 Configure error handling and logging infrastructure in backend/src/core/config.py
- [X] T010 Setup environment configuration management in backend/src/core/config.py
- [X] T011 [P] Configure Better Auth in frontend/src/lib/auth.ts
- [X] T012 [P] Set up API client for backend communication in frontend/src/lib/api.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Allow new users to create an account using their email and password

**Independent Test**: Can be fully tested by navigating to the registration page, filling in user details, and verifying that an account is created and the user can log in with those credentials.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Contract test for POST /api/v1/auth/register in backend/tests/contract/test_auth.py
- [X] T014 [P] [US1] Unit test for User model validation in backend/tests/unit/test_user_model.py

### Implementation for User Story 1

- [X] T015 [P] [US1] Create User model in backend/src/models/user.py
- [X] T016 [US1] Implement UserService for user creation in backend/src/services/user_service.py
- [X] T017 [US1] Implement registration endpoint in backend/src/api/auth.py
- [X] T018 [US1] Add validation and error handling for registration in backend/src/api/auth.py
- [X] T019 [US1] Create SignupForm component in frontend/src/components/auth/SignupForm.tsx
- [X] T020 [US1] Implement signup page in frontend/src/app/auth/signup/page.tsx
- [X] T021 [US1] Add navigation link to signup page in frontend/src/components/layout/Navbar.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Login (Priority: P1)

**Goal**: Allow existing users to log in to access their account and protected resources

**Independent Test**: Can be fully tested by navigating to the login page, entering valid credentials, and verifying that the user is authenticated and granted access to protected resources.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T022 [P] [US2] Contract test for POST /api/v1/auth/login in backend/tests/contract/test_auth.py
- [X] T023 [P] [US2] Integration test for login flow in backend/tests/integration/test_auth.py

### Implementation for User Story 2

- [X] T024 [P] [US2] Implement JWT token creation in backend/src/core/security.py
- [X] T025 [US2] Implement login endpoint in backend/src/api/auth.py
- [X] T026 [US2] Implement logout endpoint in backend/src/api/auth.py
- [X] T027 [US2] Create LoginForm component in frontend/src/components/auth/LoginForm.tsx
- [X] T028 [US2] Implement login page in frontend/src/app/auth/signin/page.tsx
- [X] T029 [US2] Implement authentication state management in frontend/src/hooks/useAuth.ts
- [X] T030 [US2] Add navigation link to login page in frontend/src/components/layout/Navbar.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Protected Resource Access (Priority: P2)

**Goal**: Ensure authenticated users can access only their own resources and protected endpoints reject unauthorized requests

**Independent Test**: Can be tested by authenticating as a user, requesting protected resources with a valid JWT token, and verifying that access is granted only to resources belonging to that user.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T031 [P] [US3] Contract test for GET /api/v1/auth/me in backend/tests/contract/test_auth.py
- [X] T032 [P] [US3] Contract test for GET /api/v1/users/{user_id} in backend/tests/contract/test_users.py
- [X] T033 [P] [US3] Integration test for user ownership validation in backend/tests/integration/test_users.py

### Implementation for User Story 3

- [X] T034 [P] [US3] Create authentication dependency in backend/src/api/deps.py
- [X] T035 [US3] Implement get current user endpoint in backend/src/api/auth.py
- [X] T036 [US3] Implement get user profile endpoint in backend/src/api/users.py
- [X] T037 [US3] Add user ownership validation middleware in backend/src/api/deps.py
- [X] T038 [US3] Create protected dashboard page in frontend/src/app/dashboard/page.tsx
- [X] T039 [US3] Implement protected route component in frontend/src/components/auth/ProtectedRoute.tsx
- [X] T040 [US3] Add API request with JWT token in frontend/src/lib/api.ts

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T041 [P] Documentation updates in docs/
- [ ] T042 Code cleanup and refactoring
- [ ] T043 Performance optimization across all stories
- [ ] T044 [P] Additional unit tests (if requested) in backend/tests/unit/
- [ ] T045 Security hardening
- [ ] T046 Run quickstart.md validation

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
Task: "Contract test for POST /api/v1/auth/register in backend/tests/contract/test_auth.py"
Task: "Unit test for User model validation in backend/tests/unit/test_user_model.py"

# Launch all models for User Story 1 together:
Task: "Create User model in backend/src/models/user.py"
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