# Tasks: AI Agent, Runner & Stateless Chat Orchestration

**Feature**: AI Agent, Runner & Stateless Chat Orchestration  
**Branch**: `011-ai-agent-runner`  
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)  
**Created**: 2026-02-11

## Overview

This document lists all tasks required to implement the AI-powered conversational agent that enables users to manage tasks using natural language. The system uses OpenAI Agents SDK to interpret user commands, integrates with MCP tools for task operations, and persists conversation state in a Neon PostgreSQL database.

## Implementation Strategy

- **MVP Scope**: Implement User Story 1 (Natural Language Task Management) with minimal viable conversation persistence
- **Incremental Delivery**: Complete each user story as a standalone, testable increment
- **Parallel Opportunities**: Models and services can often be developed in parallel
- **Testing Approach**: Unit tests for services, integration tests for API endpoints

---

## Phase 1: Setup

_Setup foundational project structure and dependencies_

- [x] T001 Create backend directory structure per plan.md
- [x] T002 Initialize Poetry project with required dependencies (FastAPI, SQLModel, asyncpg, openai, python-multipart)
- [x] T003 Configure settings module with environment variables for API keys and database
- [x] T004 Set up database connection and async session factory
- [x] T005 Create base SQLModel classes and database initialization
- [x] T006 Set up Alembic for database migrations
- [x] T007 Configure logging and error handling middleware

---

## Phase 2: Foundational Components

_Common components required by all user stories_

- [x] T008 [P] Create Conversation model in `backend/src/models/conversation.py` per data-model.md
- [x] T009 [P] Create Message model in `backend/src/models/conversation.py` per data-model.md
- [x] T010 [P] Create database utility functions for CRUD operations on conversations and messages
- [x] T011 [P] Implement conversation service in `backend/src/services/conversation_service.py`
- [x] T012 [P] Create API dependencies module in `backend/src/api/deps.py` for authentication
- [x] T013 [P] Create base API router in `backend/src/api/base_router.py`
- [x] T014 [P] Set up database migration for conversations and messages tables

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1)

_As a user, I want to manage my tasks using natural language through the chat interface so that I can express my intentions in plain English without needing to learn specific commands. When I say something like "Add a task to buy groceries," the AI agent should understand my intent and create the task for me._

**Independent Test**: Can be fully tested by sending natural language commands to the chat API and verifying that the AI agent correctly interprets the intent and performs the appropriate task operations via MCP tools.

**Acceptance Scenarios**:
1. Given a user sends a natural language command like "Add a task to buy groceries," when the message is processed by the AI agent, then the agent creates a new task titled "buy groceries" using the MCP tools.
2. Given a user sends a command like "Mark the grocery task as completed," when the message is processed by the AI agent, then the agent identifies the correct task and marks it as completed using the MCP tools.

### Phase 3.1: Core Agent Infrastructure

- [x] T015 [US1] Create OpenAI client configuration in `backend/src/config/openai_config.py`
- [x] T016 [US1] Implement MCP integration service in `backend/src/services/mcp_integration.py`
- [x] T017 [US1] Define system prompt for task management agent in `backend/src/config/prompts.py`
- [x] T018 [US1] Create agent runner service in `backend/src/services/agent_runner.py`
- [x] T019 [US1] Implement tool registration mechanism for MCP tools in agent runner

### Phase 3.2: API Implementation

- [x] T020 [US1] Create chat router in `backend/src/api/chat_router.py`
- [x] T021 [US1] Implement POST /api/{user_id}/chat endpoint in chat router
- [x] T022 [US1] Add request/response models for chat API in `backend/src/models/chat.py`
- [x] T023 [US1] Connect agent runner to chat endpoint
- [x] T024 [US1] Implement conversation context building in agent runner
- [x] T025 [US1] Add error handling for agent execution failures

### Phase 3.3: Integration & Testing

- [x] T026 [US1] Write integration tests for chat endpoint with natural language commands
- [x] T027 [US1] Test conversation persistence with message history
- [x] T028 [US1] Verify MCP tool calls are properly invoked from agent
- [x] T029 [US1] Test error handling when MCP tools fail

---

## Phase 4: User Story 2 - Persistent Conversation Context (Priority: P1)

_As a user, I want my conversation with the AI agent to maintain context so that I can have a natural, flowing conversation without repeating myself. The system should remember what we've discussed previously and allow me to continue from where we left off._

**Independent Test**: Can be fully tested by starting a conversation, performing several task operations, ending the session, and then resuming the conversation to verify that the AI agent remembers the context and can continue appropriately.

**Acceptance Scenarios**:
1. Given a user has an ongoing conversation with the AI agent, when the user refers to a previously mentioned task without specifying its name, then the agent correctly identifies the intended task based on conversation history.
2. Given a user refreshes the page or closes and reopens the application, when the user resumes the conversation, then the AI agent continues from where the conversation left off.

### Phase 4.1: Context Management

- [x] T030 [US2] Enhance conversation service to retrieve full conversation history
- [x] T031 [US2] Implement message serialization for agent context
- [x] T032 [US2] Add conversation metadata handling (titles, state)
- [x] T033 [US2] Update agent runner to properly maintain conversation context

### Phase 4.2: API Enhancement

- [x] T034 [US2] Enhance chat API to handle conversation continuation
- [x] T035 [US2] Add conversation_id validation and error handling
- [x] T036 [US2] Implement conversation state management (active, archived)

### Phase 4.3: Integration & Testing

- [x] T037 [US2] Write tests for conversation context preservation
- [x] T038 [US2] Test conversation resumption after interruption
- [x] T039 [US2] Verify context is properly passed to agent across requests

---

## Phase 5: User Story 3 - Reliable Task Operations (Priority: P2)

_As a user, I want to be confident that my task management operations are reliable and that I receive clear feedback about the results so that I can trust the system to correctly handle my tasks._

**Independent Test**: Can be fully tested by performing various task operations and verifying that the AI agent provides appropriate feedback for both successful operations and error conditions.

**Acceptance Scenarios**:
1. Given a user performs a task operation, when the operation completes successfully, then the AI agent confirms the success in natural language.
2. Given a user performs an operation that encounters an error, when the operation fails, then the AI agent provides a helpful error message that guides the user toward resolution.

### Phase 5.1: Error Handling & Feedback

- [x] T040 [US3] Implement error handling wrapper for MCP tool calls
- [x] T041 [US3] Create standardized error response format for agent
- [x] T042 [US3] Enhance agent runner with error recovery mechanisms
- [x] T043 [US3] Add user-friendly error messaging in agent responses

### Phase 5.2: Response Formatting

- [x] T044 [US3] Implement response formatter for ChatKit UI compatibility
- [x] T045 [US3] Add success confirmation messages for task operations
- [x] T046 [US3] Create response templates for different operation types

### Phase 5.3: Integration & Testing

- [x] T047 [US3] Test error handling scenarios with MCP tool failures
- [x] T048 [US3] Verify success confirmations are properly formatted
- [x] T049 [US3] Test graceful degradation when tools are unavailable

---

## Phase 6: Polish & Cross-Cutting Concerns

_Final touches and optimizations_

- [x] T050 Add comprehensive logging for agent operations and tool calls
- [x] T051 Implement rate limiting for chat API endpoints
- [x] T052 Add performance monitoring for agent response times
- [x] T053 Write end-to-end tests covering all user stories
- [x] T054 Document API endpoints with Swagger/OpenAPI
- [x] T055 Optimize database queries for conversation/message retrieval
- [x] T056 Add input sanitization and security validation
- [x] T057 Create deployment configuration for production

---

## Dependencies

### User Story Completion Order
1. US1 (Natural Language Task Management) - Foundation for all other stories
2. US2 (Persistent Conversation Context) - Builds on US1's infrastructure
3. US3 (Reliable Task Operations) - Enhances error handling across all stories

### Critical Path
T001 → T002 → T003 → T004 → T005 → T006 → T008 → T009 → T010 → T011 → T015 → T016 → T017 → T018 → T020 → T021 → T022 → T023

---

## Parallel Execution Examples

### Per Story Parallelization
**US1 - Natural Language Task Management**:
- T015 [P] [US1] OpenAI client configuration
- T016 [P] [US1] MCP integration service
- T017 [P] [US1] System prompt definition
- T018 [P] [US1] Agent runner service

**US2 - Persistent Conversation Context**:
- T030 [P] [US2] Enhanced conversation service
- T031 [P] [US2] Message serialization
- T032 [P] [US2] Metadata handling

**US3 - Reliable Task Operations**:
- T040 [P] [US3] Error handling wrapper
- T041 [P] [US3] Standardized error responses
- T044 [P] [US3] Response formatter