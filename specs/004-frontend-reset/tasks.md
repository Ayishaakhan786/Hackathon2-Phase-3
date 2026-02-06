# Tasks: Frontend Reset & Proper Next.js Initialization

**Input**: Design documents from `/specs/004-frontend-reset/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

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

- [X] T001 Remove existing frontend directory and all its contents from project root
- [X] T002 [P] Initialize new Next.js project with App Router using `npx create-next-app@latest` in project root
- [X] T003 [P] Configure project with TypeScript, ESLint, and Tailwind CSS as recommended
- [X] T004 Verify project structure matches Next.js 16+ App Router template

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T005 Set up proper gitignore for frontend directory with Node.js patterns
- [X] T006 [P] Configure Next.js settings in next.config.ts per project requirements
- [X] T007 [P] Set up TypeScript configuration in tsconfig.json per Next.js standards
- [X] T008 Configure ESLint with recommended Next.js and TypeScript settings
- [X] T009 Set up basic project structure in app/ directory with layout.tsx and page.tsx
- [X] T010 [P] Add necessary dependencies for the project as specified in plan.md
- [X] T011 Create public directory and basic assets
- [X] T012 Set up environment configuration for API connections

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Clean Next.js Project Access (Priority: P1) 🎯 MVP

**Goal**: Ensure developers have access to a properly initialized Next.js project that runs without errors

**Independent Test**: Can be verified by running `npm install` followed by `npm run dev` in the frontend directory and confirming that the default Next.js welcome page loads without errors.

### Implementation for User Story 1

- [X] T013 Verify development server runs without errors using `npm run dev`
- [X] T014 [P] Ensure default Next.js welcome page is accessible at root URL
- [X] T015 Confirm project structure includes standard Next.js directories (app/, public/, etc.)
- [X] T016 Validate configuration files follow Next.js conventions (package.json, next.config.js, etc.)
- [X] T017 Test that build process completes successfully with `npm run build`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Standard Development Workflow (Priority: P1)

**Goal**: Enable developers to follow standard Next.js App Router patterns for creating pages and using framework features

**Independent Test**: Can be verified by creating a simple page in the app directory and confirming it renders correctly following App Router conventions.

### Implementation for User Story 2

- [ ] T018 [P] Create sample page in app/sample/page.tsx following App Router conventions
- [ ] T019 Implement routing test to verify file-based routing works correctly
- [ ] T020 Test Next.js features like next/link work as documented
- [ ] T021 Create a basic layout in app/layout.tsx
- [ ] T022 Add global styles in app/globals.css

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Maintainable Project Structure (Priority: P2)

**Goal**: Ensure the project follows Next.js best practices with a clean, standard structure that supports future development

**Independent Test**: Can be verified by checking that the project follows Next.js best practices and doesn't contain any unnecessary or custom files.

### Implementation for User Story 3

- [ ] T023 Verify project structure matches standard Next.js 16+ App Router template exactly
- [ ] T024 [P] Remove any extraneous files that don't follow Next.js conventions
- [ ] T025 Test that new dependencies integrate properly with Next.js build system
- [ ] T026 Validate that linting and type checking pass without errors
- [ ] T027 Create documentation for the project structure in README.md

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T028 [P] Update main README with frontend setup instructions
- [ ] T029 Add documentation for common tasks in docs/frontend-setup.md
- [ ] T030 Run quickstart.md validation to ensure accuracy
- [ ] T031 Final verification that all success criteria are met
- [ ] T032 Clean up temporary files or test implementations

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
# Launch all components for User Story 1 together:
Task: "Verify development server runs without errors using npm run dev"
Task: "Ensure default Next.js welcome page is accessible at root URL"
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
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence