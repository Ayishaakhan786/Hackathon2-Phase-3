# Research: Fix 401 Unauthorized on Task Creation

## Overview
This research document outlines the current authentication implementation in the backend and identifies the specific changes needed to temporarily disable authentication for task endpoints during hackathon mode.

## Current Authentication Implementation

### Location of Task Routes
- File: `/backend/src/api/tasks.py`
- Contains all task-related endpoints with authentication dependencies

### Authentication Dependencies Identified
After examining the codebase, I found the following authentication dependencies in the task routes:

1. **get_current_user dependency**: Applied to all task endpoints via `Depends(get_current_user)`
2. **get_async_session dependency**: Applied to all task endpoints via `Depends(get_async_session)` (this is for database session, not authentication)
3. **HTTPBearer security**: Defined in `/backend/src/api/deps.py`

### Specific Endpoints with Authentication
All endpoints in `/backend/src/api/tasks.py` currently have the authentication dependency:
- `GET /{user_id}/tasks` - Requires authentication
- `POST /{user_id}/tasks` - Requires authentication
- `GET /{user_id}/tasks/{task_id}` - Requires authentication
- `PUT /{user_id}/tasks/{task_id}` - Requires authentication
- `DELETE /{user_id}/tasks/{task_id}` - Requires authentication
- `PATCH /{user_id}/tasks/{task_id}/complete` - Requires authentication

## Decision: Authentication Removal Strategy

### Rationale
The goal is to temporarily disable authentication for task endpoints during hackathon mode while keeping the code clean and reversible. The approach will be to modify the route handler function signatures to remove the `current_user: User = Depends(get_current_user)` parameter and adjust the internal logic that validates user permissions.

### Approach
1. Remove the `current_user: User = Depends(get_current_user)` parameter from task route handlers
2. Modify the logic that validates user permissions (currently checking if `current_user.id != user_id`)
3. Keep the `db_session: AsyncSession = Depends(get_async_session)` dependency as it's for database session management, not authentication
4. Comment out the authentication-dependent code rather than deleting it for easy restoration later

### Alternatives Considered

#### Alternative 1: Environment-based conditional authentication
- Would involve checking an environment variable to determine whether to apply authentication
- Pros: More elegant, no commented code
- Cons: Adds complexity to the codebase, requires additional configuration

#### Alternative 2: Create separate endpoints without authentication
- Would involve duplicating all task endpoints without authentication
- Pros: Keeps original endpoints intact
- Cons: Duplicates code, maintenance overhead

#### Alternative 3: Comment out authentication dependencies (Selected)
- Simply comment out the authentication-related code
- Pros: Simple, reversible, minimal changes
- Cons: Leaves commented code in the codebase temporarily

## Implementation Plan

For each task endpoint in `/backend/src/api/tasks.py`:
1. Remove or comment out the `current_user: User = Depends(get_current_user)` parameter
2. Comment out the user ID validation logic that compares `current_user.id` with `user_id`
3. Adjust the service calls to work without the current user validation (for the hackathon mode)

## Files to Modify

1. `/backend/src/api/tasks.py` - Main file to modify authentication dependencies
2. Potentially `/backend/src/api/deps.py` - If we need to modify the get_current_user function

## Expected Outcome

After the changes:
- Task endpoints will no longer require authentication
- Swagger UI will not show lock icons for task endpoints
- POST and GET requests to task endpoints will succeed without Authorization header
- Other endpoints will continue to require authentication
- Code will be easily reversible by uncommenting the authentication code