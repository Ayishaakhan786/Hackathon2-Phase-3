# Implementation Plan: Fix 401 Unauthorized on Task Creation (Auth Blocking Issue)

**Branch**: `008-fix-task-auth` | **Date**: February 6, 2026 | **Spec**: [link to spec](spec.md)
**Input**: Feature specification from `/specs/008-fix-task-auth/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Temporarily disable authentication for task endpoints during hackathon mode to allow task creation from Swagger UI and frontend without authentication. This involves removing authentication dependencies from task route handlers while preserving authentication for other endpoints. The solution must be clean and reversible for production deployment.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, asyncpg, Neon PostgreSQL
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: Web application (backend API)
**Performance Goals**: Standard web API performance expectations
**Constraints**: Must maintain security for other endpoints, code must be easily reversible
**Scale/Scope**: Hackathon development environment with temporary relaxation of auth requirements

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Potential Violation**: The feature temporarily violates the "Security-first design" principle which mandates authentication on all API endpoints. However, this is justified for the hackathon mode where rapid development and testing are prioritized over security. The change is temporary and reversible.

**Justification**: This is a temporary measure for hackathon development mode only. Authentication will be re-enabled in production. The change is isolated to specific task endpoints and preserves security for all other endpoints.

**Post-Design Re-check**: The design maintains the temporary relaxation of authentication for task endpoints during hackathon mode. This is acceptable as it serves the specific development purpose and is clearly documented as temporary. The implementation will include clear indicators that this is a temporary state and not suitable for production.

## Project Structure

### Documentation (this feature)

```text
specs/008-fix-task-auth/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

backend/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   │   ├── tasks.py
│   │   ├── deps.py
│   │   └── ...
│   └── core/
│       ├── database.py
│       └── ...
└── tests/

**Structure Decision**: This is a backend API modification affecting the task endpoints in the existing web application structure. The change involves modifying the task route handlers in the backend/src/api/tasks.py file and potentially the dependency injection in backend/src/api/deps.py.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Security-first design (temporarily) | Hackathon development mode requires relaxed security for rapid prototyping | Would slow down development if full auth was required upfront |
