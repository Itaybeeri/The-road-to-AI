# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession
from shared.db.db import get_engine
from ..services import tasks
from ..schemas.task import TaskCreate, TaskRead

engine = get_engine()
router = APIRouter(prefix="/api")

@router.get("/health")
async def health_check():
    return await {"status": "ok"}

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

@router.post("/tasks", response_model=TaskRead)
async def create(task: TaskCreate, session: Session = Depends(get_session)):
    return await tasks.create_task(session, task.name)

@router.get("/tasks/{task_id}", response_model=TaskRead)
async def read(task_id: str, session: Session = Depends(get_session)):
    task = tasks.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await task

@router.get("/tasks", response_model=list[TaskRead])
async def read_all(session: Session = Depends(get_session)):
    return await tasks.list_tasks(session)
