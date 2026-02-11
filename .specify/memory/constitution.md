# Project Constitution: Phase III – AI-Powered Todo Chatbot with MCP

## Governance Information
- **RATIFICATION_DATE**: 2026-02-11
- **LAST_AMENDED_DATE**: 2026-02-11
- **CONSTITUTION_VERSION**: 1.0.0
- **AMENDMENT_PROCEDURE**: Requires majority consensus of active contributors with 48-hour review period

## Mission Statement
Build a production-grade, AI-powered conversational Todo system that allows users to manage tasks using natural language. The system must be stateless at the server level, persist all state in a PostgreSQL database, and use MCP (Model Context Protocol) tools invoked by AI agents to perform task operations.

## Core Principles (Non-Negotiable)

### 1. Stateless Server Architecture
- No in-memory state is allowed in FastAPI, Agents, or MCP tools
- All conversation context must be fetched from and stored in the database per request

### 2. Clear Separation of Responsibilities
- FastAPI: HTTP API layer only
- OpenAI Agents SDK: reasoning, intent detection, tool orchestration
- MCP Server: exposes task operations as tools only
- Database: single source of truth for tasks, conversations, and messages

### 3. Tool-Driven Task Management
- AI agents must NEVER manipulate the database directly
- All task operations MUST go through MCP tools
- MCP tools themselves must be stateless and database-backed

### 4. Deterministic, Auditable Behavior
- Every user message and assistant response must be persisted
- Every MCP tool invocation must be traceable
- Agent decisions must be explainable via tool_calls

### 5. Hackathon-Safe Simplicity
- No premature optimization
- No over-engineering
- Prefer clarity and correctness over abstraction depth

## Technology Constraints (Must Use)
- Backend Framework: FastAPI (Python)
- ORM: SQLModel (async)
- Database: Neon Serverless PostgreSQL
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- Frontend: OpenAI ChatKit
- Authentication: Better Auth

## Data Integrity Rules
- All database writes must be transactional
- user_id is required for all task, conversation, and message records
- Conversations must survive server restarts
- Duplicate task creation must be avoided where reasonably possible

## AI Behavior Rules
- The assistant must always confirm user actions in natural language
- The assistant must never expose internal implementation details
- Errors must be handled gracefully and explained clearly to the user
- Ambiguous user requests must be resolved via reasonable assumptions, not follow-up questions

## Scope Control

### IN SCOPE:
- Conversational task management
- MCP tool-based task operations
- Stateless chat endpoint
- Conversation persistence

### OUT OF SCOPE:
- Frontend UI styling
- Real-time streaming responses
- Background jobs or schedulers
- Multi-agent coordination

## Quality Bar
- Code must be readable and modular
- Architecture must be easy to explain to judges
- Authentication can be temporarily relaxed for hackathon testing, but must be reversible
- System must function correctly after server restart without data loss

## Success Criteria
- Users can manage todos using natural language
- AI agent correctly maps intent to MCP tools
- Conversations resume correctly after restart
- No task operation bypasses MCP tools
- System behaves predictably and reliably under repeated requests

## Amendment Log
- v1.0.0 (2026-02-11): Initial constitution for Phase III – AI-Powered Todo Chatbot