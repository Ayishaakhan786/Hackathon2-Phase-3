<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.1.0
Modified principles: [PRINCIPLE_1_NAME] → Security-first design, [PRINCIPLE_2_NAME] → Spec-driven development, [PRINCIPLE_3_NAME] → Separation of concerns, [PRINCIPLE_4_NAME] → Scalability & maintainability, [PRINCIPLE_5_NAME] → User-centric experience
Added sections: Key Standards, Constraints, API Constraints, Agent Responsibilities, Success Criteria
Removed sections: Template placeholders
Templates requiring updates: ✅ Updated all
Follow-up TODOs: None
-->
# Hackathon-2 Phase-2 Constitution

## Core Principles

### Security-first design
Authentication, authorization, and data isolation are mandatory at every layer. All API endpoints must be secured with JWT-based authentication, and each user may access only their own data. No hardcoded credentials or secrets in source code are permitted.

### Spec-driven development
All implementation must follow clearly defined specifications using Claude Code + Spec-Kit Plus. Every feature must be planned, specified, and validated against requirements before implementation begins.

### Separation of concerns
Frontend, backend, authentication, and database responsibilities must remain clearly separated. Backend and frontend must be loosely coupled, with clean API contracts defining their interactions.

### Scalability & maintainability
Architecture should support future feature expansion with minimal refactoring. Code must follow framework best practices and conventions, with clear error handling and proper HTTP status codes.

### User-centric experience
The application must be intuitive, responsive, and accessible across devices. Frontend must use Next.js 16+ App Router with responsive layout and components that provide a seamless user experience.

### Data integrity
Persistent storage must maintain consistency and reliability. Database access must use SQLModel ORM with proper transaction handling and validation to prevent data corruption.

## Key Standards

- All API endpoints must be **RESTful and documented**
- JWT-based authentication must be enforced on **every protected endpoint**
- Each user may access **only their own data**
- Frontend must use **Next.js 16+ App Router**
- Backend must use **Python FastAPI**
- Database access must use **SQLModel ORM**
- Persistent storage must be **Neon Serverless PostgreSQL**
- Authentication must use **Better Auth** with JWT tokens
- Code must follow framework best practices and conventions
- Clear error handling and proper HTTP status codes are required

## Constraints

- Application must implement **all 5 Basic Level features**
- Architecture must support **multi-user usage**
- Backend and frontend must be **loosely coupled**
- Authentication logic must not leak secrets to the frontend
- No hardcoded credentials or secrets in source code
- All protected API routes must require valid JWT tokens

## API Constraints

- Base path: `/api/{user_id}`
- Supported methods: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
- Endpoints must enforce:
  - Authentication (JWT verification)
  - Authorization (user ownership validation)

## Agent Responsibilities

- **Auth Agent**
  - Better Auth integration
  - JWT issuing and validation strategy
  - Security standards enforcement

- **Backend Agent**
  - FastAPI REST API implementation
  - JWT verification and authorization logic
  - Business rules and data validation

- **DB Agent**
  - SQLModel schema design
  - Neon PostgreSQL integration
  - Data integrity and relationships

- **Frontend Agent**
  - Next.js App Router UI development
  - Responsive layout and components
  - Auth-aware routing and API consumption

## Success Criteria

- Users can sign up and sign in securely
- JWT-secured API communication works end-to-end
- Each user can only view and modify their own tasks
- All task CRUD operations function correctly
- Data persists across sessions and reloads
- Frontend is responsive and accessible
- No unauthorized API access is possible
- System passes functional and security review

## Governance

This constitution governs all development activities for the Hackathon-2 Phase-2 project. All implementation must comply with the stated principles and standards. Amendments to this constitution require team consensus and must be documented with clear justification. All pull requests and reviews must verify compliance with these principles.

**Version**: 1.1.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06