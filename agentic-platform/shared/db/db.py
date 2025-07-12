# app/db.py
import os
import re
import asyncio
import asyncpg
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

# Parse DATABASE_URL for credentials
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://docker:docker@localhost/agentic_db")
match = re.match(r"postgresql\+asyncpg://([^:]+):([^@]+)@([^:/]+)(?::(\d+))?/([^?]+)", DATABASE_URL)
if match:
    user, password, host, port, db_name = match.groups()
    port = int(port) if port else 5432
    
    async def ensure_database_exists():
        conn = await asyncpg.connect(user=user, password=password, database='postgres', host=host, port=port)
        db_exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", db_name)
        if not db_exists:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
        await conn.close()
    # Ensure DB exists before engine creation
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # If there's a running loop, schedule the coroutine and wait for it
        import nest_asyncio
        nest_asyncio.apply()
        task = loop.create_task(ensure_database_exists())
        loop.run_until_complete(task)
    else:
        asyncio.run(ensure_database_exists())
else:
    raise ValueError("Invalid DATABASE_URL format")

def get_engine():
    return create_async_engine(DATABASE_URL, echo=True, future=True)
