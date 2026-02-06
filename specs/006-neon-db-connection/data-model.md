# Data Model: Neon PostgreSQL Database Connection

## Database Connection Entity

**Description**: Represents the connection to the Neon PostgreSQL database with proper SSL configuration

**Configuration Properties**:
- `database_url`: string | connection string with SSL parameters (sslmode=require)
- `pool_size`: integer | number of connections to maintain in the pool (default: 5)
- `max_overflow`: integer | additional connections beyond pool_size (default: 10)
- `pool_pre_ping`: boolean | verify connections before use (default: True)
- `echo`: boolean | enable SQL query logging (default: False based on DEBUG env var)

**Validation Rules**:
- `database_url` must follow PostgreSQL connection string format
- `database_url` must include sslmode=require parameter
- `pool_size` must be between 1 and 50
- `max_overflow` must be between 0 and 50

## Connection Pool Entity

**Description**: Manages multiple database connections efficiently to handle concurrent requests

**Properties**:
- `active_connections`: integer | number of currently active connections
- `max_connections`: integer | maximum allowed connections (default: 20)
- `idle_timeout`: integer | time before idle connections are closed (default: 300 seconds)
- `health_status`: enum | current status (healthy, degraded, unhealthy)

**Operations**:
- Acquire connection: Retrieve a connection from the pool
- Release connection: Return a connection to the pool after use
- Monitor health: Check the health status of the connection pool
- Scale pool: Adjust pool size based on demand

## Environment Configuration Entity

**Description**: Stores database credentials and connection parameters securely in environment variables

**Properties**:
- `DATABASE_URL`: string | full connection string with credentials
- `DEBUG`: boolean | enable debug mode (default: False)
- `LOG_LEVEL`: string | logging level (default: info)
- `API_HOST`: string | host address for the API (default: 0.0.0.0)
- `API_PORT`: integer | port number for the API (default: 8000)

**Validation Rules**:
- `DATABASE_URL` must not be empty
- `DATABASE_URL` must be a valid PostgreSQL connection string
- `API_PORT` must be between 1024 and 65535