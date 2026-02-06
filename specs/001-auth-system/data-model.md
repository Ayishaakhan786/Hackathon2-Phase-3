# Data Model: Authentication & User Foundation

**Date**: 2026-02-06
**Feature**: Authentication & User Foundation
**Branch**: 001-auth-system

## Overview

This document defines the data models required for the authentication system, focusing on user management and authentication-related entities.

## User Entity

### Attributes
- **id** (UUID/Integer): Unique identifier for the user
- **email** (String): User's email address (unique, required)
- **hashed_password** (String): BCrypt-hashed password (required)
- **created_at** (DateTime): Timestamp when the account was created
- **updated_at** (DateTime): Timestamp when the account was last updated
- **is_active** (Boolean): Whether the account is active (default: true)
- **is_verified** (Boolean): Whether the email has been verified (default: false)

### Relationships
- **Tasks** (one-to-many): A user can have many tasks
- **Sessions** (one-to-many): A user can have multiple active sessions (if implementing session tracking)

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum strength requirements
- Email cannot be changed after account creation (for simplicity)

## JWT Token Structure

### Claims
- **sub** (Subject): User ID
- **email**: User's email address
- **exp** (Expiration Time): Token expiration timestamp
- **iat** (Issued At): Token creation timestamp
- **jti** (JWT ID): Unique identifier for the token (for blacklisting if needed)

### Token Properties
- **Algorithm**: RS256 (RSA Signature with SHA-256)
- **Expiration**: 15 minutes for access tokens
- **Refresh Token**: 7 days (to be implemented in future iteration)

## Session Entity (Optional - for enhanced security)

### Attributes
- **id** (UUID): Unique identifier for the session
- **user_id** (UUID/Integer): Reference to the user
- **token_hash** (String): Hash of the session token
- **expires_at** (DateTime): Expiration timestamp
- **created_at** (DateTime): Creation timestamp
- **last_accessed** (DateTime): Last time the session was used
- **device_info** (String): Information about the device used
- **ip_address** (String): IP address of the client

### Relationships
- **User** (many-to-one): The user associated with this session

## State Transitions

### User Account States
1. **Pending** (Implicit): After registration, before email verification
2. **Active**: After email verification, account is fully functional
3. **Deactivated**: User deactivated their account
4. **Suspended**: Admin suspended the account (for violations)

### Transition Rules
- Pending → Active: After successful email verification
- Active → Deactivated: When user chooses to deactivate account
- Active → Suspended: When admin suspends the account
- Deactivated → Active: When user reactivates their account
- Suspended → Active: When admin reactivates the account

## Constraints

### Data Integrity
- Email uniqueness constraint at database level
- Password cannot be null for active users
- Created_at and updated_at timestamps automatically managed

### Security
- Passwords must be hashed before storing
- No plaintext passwords in the database
- User IDs should be non-sequential to prevent enumeration attacks
- Email verification required before certain actions (TBD based on business requirements)