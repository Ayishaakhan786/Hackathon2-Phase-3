# API Contract: Database Health Check

## Endpoint: GET /health/db

### Purpose
Verify that the application can successfully connect to the Neon PostgreSQL database.

### Request
- Method: GET
- Path: `/health/db`
- Headers: None required
- Query Parameters: None
- Body: None

### Response

#### Success Response (200 OK)
```json
{
  "status": "healthy",
  "timestamp": "2026-02-06T16:15:30.123456Z",
  "database": {
    "connected": true,
    "version": "PostgreSQL 15.2 (Neon)",
    "ssl_enabled": true
  }
}
```

#### Error Response (503 Service Unavailable)
```json
{
  "status": "unhealthy",
  "timestamp": "2026-02-06T16:15:30.123456Z",
  "database": {
    "connected": false,
    "error": "Connection refused",
    "details": "Unable to connect to Neon PostgreSQL database"
  }
}
```

### Implementation Requirements
- Execute a simple query (e.g., SELECT 1) to verify connectivity
- Include database version information if available
- Verify SSL connection is enabled
- Respond within 2 seconds
- Log connection status for monitoring

## Endpoint: GET /health

### Purpose
General application health check that includes database connectivity.

### Request
- Method: GET
- Path: `/health`
- Headers: None required
- Query Parameters: None
- Body: None

### Response

#### Success Response (200 OK)
```json
{
  "status": "healthy",
  "timestamp": "2026-02-06T16:15:30.123456Z",
  "checks": {
    "database": "healthy",
    "api_server": "running"
  }
}
```

#### Partial Success Response (207 Multi-Status)
```json
{
  "status": "degraded",
  "timestamp": "2026-02-06T16:15:30.123456Z",
  "checks": {
    "database": "unhealthy",
    "api_server": "running"
  }
}
```