from decouple import config
import os
import re

# Load environment variables from .env file
DATABASE_URL = config('DATABASE_URL', default='')
API_HOST = config('API_HOST', default='0.0.0.0')
API_PORT = config('API_PORT', cast=int, default=8000)
DEBUG = config('DEBUG', cast=bool, default=False)
LOG_LEVEL = config('LOG_LEVEL', default='info')

# Validation
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Validate DATABASE_URL format (should be a valid PostgreSQL connection string)
if not re.match(r'^postgresql://', DATABASE_URL):
    raise ValueError("DATABASE_URL must be a valid PostgreSQL connection string")

# Validate API_PORT range (1024-65535)
if not (1024 <= API_PORT <= 65535):
    raise ValueError("API_PORT must be between 1024 and 65535")

# Additional validation for sslmode=require in DATABASE_URL
if 'sslmode=require' not in DATABASE_URL:
    raise ValueError("DATABASE_URL must include sslmode=require for Neon PostgreSQL")