# Quickstart Guide: Neon PostgreSQL Database Connection

## Prerequisites

- Python 3.11+ installed
- PostgreSQL database hosted on Neon
- Valid DATABASE_URL with sslmode=require
- pip package manager

## Setup Instructions

1. Ensure your environment variables are properly set in backend/.env:
   ```
   DATABASE_URL=postgresql://<user>:<password>@<neon-host>/<dbname>?sslmode=require
   API_HOST=0.0.0.0
   API_PORT=8000
   DEBUG=false
   LOG_LEVEL=info
   ```

2. Install required dependencies:
   ```bash
   pip install sqlmodel sqlalchemy psycopg2-binary python-decouple
   ```

3. Verify the database connection by running the health check:
   ```bash
   python -c "from backend.src.database.connection import engine; print('Engine created successfully')"
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

2. Verify database connectivity by accessing the health check endpoint:
   ```
   GET http://localhost:8000/health/db
   ```

## Key Files

- `backend/src/database/connection.py` - Database connection setup and configuration
- `backend/src/config/settings.py` - Environment variable loading
- `backend/src/api/health.py` - Health check endpoints
- `backend/.env` - Environment configuration

## Troubleshooting

- If you get SSL connection errors, ensure sslmode=require is in your DATABASE_URL
- If you get authentication errors, verify your username and password in DATABASE_URL
- If you get connection timeout errors, check your network connection to Neon