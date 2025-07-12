# app/services/tasks.py
from sqlmodel import Session, select
from shared.models.task import Task

async def create_task(session: Session, name: str) -> Task:
    task = Task(name=name)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_task(session: Session, task_id: str) -> Task:
    return await session.get(Task, task_id)

async def list_tasks(session: Session) -> list[Task]:
    result = await session.exec(select(Task))
    return result.all()
