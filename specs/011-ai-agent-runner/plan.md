# Implementation Plan: AI Agent, Runner & Stateless Chat Orchestration

**Branch**: `011-ai-agent-runner` | **Date**: 2026-02-11 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/011-ai-agent-runner/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This implementation plan outlines the development of an AI-powered conversational agent that enables users to manage tasks using natural language. The system uses OpenAI Agents SDK to interpret user commands, integrates with MCP tools for task operations, and persists conversation state in a Neon PostgreSQL database. The architecture follows a stateless design where each API request fetches conversation context from the database, ensuring no in-memory state is maintained between requests. This approach satisfies the constitutional requirement for a stateless server architecture while maintaining conversation continuity.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: OpenAI Agents SDK, FastAPI, SQLModel, asyncpg, Neon PostgreSQL, MCP SDK
**Storage**: Neon Serverless PostgreSQL database with async SQLModel ORM
**Testing**: pytest for backend testing
**Target Platform**: Linux server environment
**Project Type**: Web application (backend service with API endpoints)
**Performance Goals**: Respond to chat requests within 5 seconds under normal load conditions
**Constraints**: Must be stateless server architecture with no in-memory state, all data persisted in database
**Scale/Scope**: Designed for multiple concurrent users with persistent conversations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification

1. **Stateless Server Architecture**: The AI Agent Runner will be implemented as a stateless service that fetches conversation context from the database for each request, in compliance with the constitution's requirement for no in-memory state.

2. **Clear Separation of Responsibilities**: The implementation will maintain clear separation between FastAPI (HTTP API layer), OpenAI Agents SDK (reasoning and tool orchestration), and MCP Server (task operations), as mandated by the constitution.

3. **Tool-Driven Task Management**: The AI agent will exclusively use MCP tools for all task operations, with no direct database access, satisfying the constitution's requirement that all task operations go through MCP tools.

4. **Deterministic, Auditable Behavior**: Every user message and assistant response will be persisted in the database, and all MCP tool invocations will be traceable through the message logs.

5. **Technology Constraints**: The implementation will use the required technologies: FastAPI, SQLModel, Neon PostgreSQL, OpenAI Agents SDK, and MCP SDK.

6. **Data Integrity**: All database operations will be performed transactionally with proper user_id validation for all records.

7. **AI Behavior Rules**: The agent will confirm user actions in natural language and handle errors gracefully as specified in the constitution.

## Project Structure

### Documentation (this feature)

```text
specs/011-ai-agent-runner/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── chat-api.yaml    # OpenAPI specification for chat API
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── pyproject.toml       # Project dependencies and configuration
├── poetry.lock          # Locked dependency versions
├── src/
│   ├── main.py          # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── conversation.py  # Conversation and Message models
│   │   └── user.py          # User model if needed
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_runner.py  # AI Agent orchestration service
│   │   ├── conversation_service.py  # Conversation management
│   │   └── mcp_integration.py       # MCP tools integration
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py        # Dependency injection utilities
│   │   └── chat_router.py # Chat API endpoints
│   └── config/
│       ├── __init__.py
│       └── settings.py    # Application settings and configuration
└── tests/
    ├── __init__.py
    ├── unit/
    ├── integration/
    └── contract/
```

**Structure Decision**: Web application structure selected as this feature implements a backend service with API endpoints for the AI agent functionality. The backend contains all the necessary components for the AI agent runner, conversation management, and MCP tool integration.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
