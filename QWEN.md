# Project Qwen - Modern Multi-User Web Application

## Objective
Using Claude Code and Spec-Kit Plus transform the console app into a modern multi-user web application with persistent storage.

## Project Requirements

### Core Features
- Implement all 5 Basic Level features as a web application
- Create RESTful API endpoints
- Build responsive frontend interface
- Store data in Neon Serverless PostgreSQL database
- Authentication – Implement user signup/signin using Better Auth

### Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+ (App Router) |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Spec-Driven | Claude Code + Spec-Kit Plus |
| Authentication | Better Auth |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## Agent Assignments

### 1. Authentication (Auth Agent)
- Implement user signup/signin functionality using Better Auth
- Configure JWT token issuance for API authentication
- Secure API endpoints with Better Auth + FastAPI integration
- Handle user sessions and authentication state

### 2. Frontend Development (NextJS UI Generator Agent)
- Build responsive frontend interface using Next.js 16+ (App Router)
- Implement UI components for task management
- Create user-friendly interfaces for all 5 basic features
- Ensure mobile-first responsive design
- Integrate with Better Auth for authentication flows

### 3. Database Design & Development (Database Agent)
- Design database schema using SQLModel
- Implement Neon Serverless PostgreSQL database structure
- Create tables for users and tasks
- Define relationships between entities
- Optimize for the specified API endpoints

### 4. Backend Development (FastAPI Backend Agent)
- Create RESTful API endpoints using FastAPI
- Implement CRUD operations for tasks
- Integrate with SQLModel for database operations
- Secure endpoints with JWT token verification
- Handle API request/response validation

## Securing the REST API: Better Auth + FastAPI Integration

### The Challenge
Better Auth is a JavaScript/TypeScript authentication library that runs on your Next.js frontend. However, your FastAPI backend is a separate Python service that needs to verify which user is making API requests.

### The Solution: JWT Tokens
Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in. These tokens are self-contained credentials that include user information and can be verified by any service that knows the secret key.

## Implementation Plan

1. **Database Layer** (Database Agent)
   - Design and implement the database schema
   - Set up Neon Serverless PostgreSQL connection
   - Create user and task models

2. **Backend Layer** (FastAPI Backend Agent)
   - Implement API endpoints
   - Connect to the database using SQLModel
   - Add JWT token verification middleware

3. **Authentication Layer** (Auth Agent)
   - Set up Better Auth with JWT configuration
   - Implement signup/signin flows
   - Configure token passing to backend

4. **Frontend Layer** (NextJS UI Generator Agent)
   - Create responsive UI components
   - Integrate with API endpoints
   - Implement authentication flows
   - Ensure all 5 basic features are accessible

This project leverages Claude Code and Spec-Kit Plus to ensure spec-driven development practices throughout the implementation process.

## Active Technologies
- Python 3.11, TypeScript/JavaScript (Next.js 16+) + Better Auth, FastAPI, SQLModel, Neon Serverless PostgreSQL (001-auth-system)
- Python 3.11 + FastAPI, SQLModel, Neon Serverless PostgreSQL, python-jose, passlib, bcrypt (002-backend-api)
- TypeScript 5.0+, JavaScript ES2022 + Next.js 16+, React 19+, Tailwind CSS, Better Auth, SWR or React Query (003-frontend-app)
- Browser localStorage/sessionStorage for session management (003-frontend-app)
- TypeScript 5.0+, JavaScript ES2022 + Next.js 16+, React 19+, Tailwind CSS, App Router (004-frontend-reset)
- Browser storage (localStorage, sessionStorage) (004-frontend-reset)
- Browser localStorage/sessionStorage for session management (UI only, no API calls) (005-frontend-todo-ui)
- Python 3.11, TypeScript 5.0+, JavaScript ES2022 + FastAPI, SQLModel, Neon Serverless PostgreSQL, python-decouple or python-dotenv, SQLAlchemy engine with connection pooling (006-neon-db-connection)
- Neon Serverless PostgreSQL database with SSL connection (006-neon-db-connection)
- Python 3.11 + FastAPI, SQLModel, asyncpg, Neon PostgreSQL (008-fix-task-auth)

## Recent Changes
- 001-auth-system: Added Python 3.11, TypeScript/JavaScript (Next.js 16+) + Better Auth, FastAPI, SQLModel, Neon Serverless PostgreSQL
