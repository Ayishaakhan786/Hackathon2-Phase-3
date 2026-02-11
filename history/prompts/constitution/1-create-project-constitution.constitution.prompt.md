---
id: 1
title: Create Project Constitution
stage: constitution
date_iso: 2026-02-11
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - governance
  - principles
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
---

# Create Project Constitution

## User Input
```
/sp.constitution Phase Name: Phase III – AI-Powered Todo Chatbot with MCP

Mission:
Build a production-grade, AI-powered conversational Todo system that allows users to manage tasks using natural language. The system must be stateless at the server level, persist all state in a PostgreSQL database, and use MCP (Model Context Protocol) tools invoked by AI agents to perform task operations.

Core Principles (Non-Negotiable):
1. Stateless Server Architecture
   - No in-memory state is allowed in FastAPI, Agents, or MCP tools
   - All conversation context must be fetched from and stored in the database per request

2. Clear Separation of Responsibilities
   - FastAPI: HTTP API layer only
   - OpenAI Agents SDK: reasoning, intent detection, tool orchestration
   - MCP Server: exposes task operations as tools only
   - Database: single source of truth for tasks, conversations, and messages

3. Tool-Driven Task Management
   - AI agents must NEVER manipulate the database directly
   - All task operations MUST go through MCP tools
   - MCP tools themselves must be stateless and database-backed

4. Deterministic, Auditable Behavior
   - Every user message and assistant response must be persisted
   - Every MCP tool invocation must be traceable
   - Agent decisions must be explainable via tool_calls

5. Hackathon-Safe Simplicity
   - No premature optimization
   - No over-engineering
   - Prefer clarity and correctness over abstraction depth

Technology Constraints (Must Use):
- Backend Framework: FastAPI (Python)
- ORM: SQLModel (async)
- Database: Neon Serverless PostgreSQL
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- Frontend: OpenAI ChatKit
- Authentication: Better Auth

Data Integrity Rules:
- All database writes must be transactional
- user_id is required for all task, conversation, and message records
- Conversations must survive server restarts
- Duplicate task creation must be avoided where reasonably possible

AI Behavior Rules:
- The assistant must always confirm user actions in natural language
- The assistant must never expose internal implementation details
- Errors must be handled gracefully and explained clearly to the user
- Ambiguous user requests must be resolved via reasonable assumptions, not follow-up questions

Scope Control:
IN SCOPE:
- Conversational task management
- MCP tool-based task operations
- Stateless chat endpoint
- Conversation persistence

OUT OF SCOPE:
- Frontend UI styling
- Real-time streaming responses
- Background jobs or schedulers
- Multi-agent coordination

Quality Bar:
- Code must be readable and modular
- Architecture must be easy to explain to judges
- Authentication can be temporarily relaxed for hackathon testing, but must be reversible
- System must function correctly after server restart without data loss

Success Criteria:
- Users can manage todos using natural language
- AI agent correctly maps intent to MCP tools
- Conversations resume correctly after restart
- No task operation bypasses MCP tools
- System behaves predictably and reliably under repeated requests
```

## Response Summary
Created the project constitution file at `.specify/memory/constitution.md` with all the specified principles, constraints, and guidelines. The constitution includes:

- Governance information with ratification date and version
- Mission statement for the AI-Powered Todo Chatbot
- Five core non-negotiable principles
- Technology constraints that must be followed
- Data integrity rules
- AI behavior rules
- Scope control (what's in and out of scope)
- Quality bar expectations
- Success criteria
- Amendment log

The constitution serves as the foundational document for the project, establishing clear guidelines and principles that all team members should follow during development.

## Outcome
The project constitution has been successfully created and saved to the appropriate location in the repository. This document will serve as the guiding framework for all development decisions throughout the project lifecycle.