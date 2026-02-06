#!/usr/bin/env python
"""
Test script to verify Neon PostgreSQL database connection.
This script tests the connection without using the async engine to avoid complications.
"""

import asyncio
import asyncpg

async def test_raw_connection():
    """Test raw connection to Neon PostgreSQL database"""
    try:
        # Extract connection parameters from the environment
        from src.core.config import settings
        import re
        
        # Parse the DATABASE_URL to extract components
        url = settings.DATABASE_URL.replace('postgresql+asyncpg://', '')
        # Split credentials and host
        parts = url.split('@')
        creds_part = parts[0]
        host_part = parts[1]
        
        # Extract username and password
        user_pass = creds_part.split(':')
        username = user_pass[0]
        password = user_pass[1].split('@')[0] if '@' in user_pass[1] else user_pass[1]
        
        # Extract database name and parameters
        host_db_params = host_part.split('/', 1)
        host_port = host_db_params[0]
        db_and_params = host_db_params[1].split('?', 1) if len(host_db_params) > 1 else [host_db_params[1], '']
        
        database = db_and_params[0]
        params_str = db_and_params[1] if len(db_and_params) > 1 else ''
        
        # Extract host and port
        host_port_parts = host_port.split(':')
        host = host_port_parts[0]
        port = host_port_parts[1] if len(host_port_parts) > 1 else '5432'
        
        print(f"Connecting to: {host}:{port}, DB: {database}, User: {username}")
        
        # Connect using asyncpg directly
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
            ssl='require'  # Use SSL as required by Neon
        )
        
        # Execute a simple query
        result = await conn.fetchval('SELECT 1')
        print(f"Query result: {result}")
        
        # Get database version
        version = await conn.fetchval('SELECT version()')
        print(f"Database version: {version}")
        
        await conn.close()
        print("Database connection test passed!")
        return True
        
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_raw_connection())
    if success:
        print("\nNeon PostgreSQL database connection is working correctly!")
    else:
        print("\nFailed to connect to Neon PostgreSQL database.")