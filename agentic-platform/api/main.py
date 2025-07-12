from fastapi import FastAPI
from api.routes.routes import router as api_router
from shared.db.db import get_engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

engine = get_engine()

@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(title="Agentic Task Automation Platform", lifespan=lifespan)

app.include_router(api_router)