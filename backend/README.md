# AI Agent Runner Backend

This is the backend service for the AI-powered conversational agent that enables users to manage tasks using natural language.

## Deployment

### Prerequisites

- Docker and Docker Compose
- Access to OpenAI API
- Access to Neon PostgreSQL database
- MCP server with task tools

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@db:5432/ai_agent_runner
OPENAI_API_KEY=your_openai_api_key
MCP_SERVER_URL=your_mcp_server_url
MCP_API_KEY=your_mcp_api_key
DB_PASSWORD=your_db_password
LOG_LEVEL=INFO
```

### Running in Production

1. Build and start the services:
   ```bash
   docker-compose up -d --build
   ```

2. The application will be available at `http://localhost` (port 80 mapped to host)

3. API documentation is available at `/docs` and `/redoc`

### Services

- **app**: Main FastAPI application
- **db**: PostgreSQL database
- **nginx**: Reverse proxy and load balancer

### SSL Configuration

To enable HTTPS, place your SSL certificates in the `ssl/` directory and update the nginx configuration accordingly.

## API Documentation

The API endpoints are automatically documented using FastAPI's integrated documentation:
- Swagger UI: `http://your-domain/docs`
- ReDoc: `http://your-domain/redoc`

## Health Check

The application provides a health check endpoint at `/health` which returns a 200 status when the service is operational.