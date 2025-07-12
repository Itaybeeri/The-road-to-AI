# app/agent/worker.py
import asyncio
from sqlmodel import select
from shared.models.task import Task
from shared.db.db import engine
from datetime import datetime

async def process_task(session, task: Task):
    print(f"Processing task: {task.id}")
    task.status = "in_progress"
    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()

    # Simulate "work"
    await asyncio.sleep(5)

    task.status = "completed"
    task.result = f"Task '{task.name}' was processed successfully"
    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()

async def agent_worker(poll_interval: int = 3):
    print("Starting agent worker...")
    from sqlmodel.ext.asyncio.session import AsyncSession

    while True:
        async with AsyncSession(engine) as session:
            result = await session.exec(
                select(Task).where(Task.status == "pending").limit(1)
            )
            task = result.first()
            if task:
                await process_task(session, task)
            else:
                await asyncio.sleep(poll_interval)
