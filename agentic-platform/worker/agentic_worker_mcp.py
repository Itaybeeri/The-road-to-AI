import sys
import os
import re
import asyncio
from datetime import datetime
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from shared.models.task import Task
from shared.db.db import get_engine
import openai
from shared.config import OPENAI_API_KEY

# Tool registry
from worker.tools.registry import get_tool_prompt_text, get_registered_tool, print_registered_tools

# Import all tools so they get registered
import worker.tools.web_summarizer  # example, add your tools here
import worker.tools.bank_account    # example, add your tools here

# Ensure correct event loop policy on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

openai.api_key = OPENAI_API_KEY

async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def call_llm(task_name: str) -> str:
    tool_text = get_tool_prompt_text()
    prompt = (
        f"You are an autonomous agent.\n"
        f"Given the task name: '{task_name}', "
        f"explain what you understand, plan your approach, and try to complete it.\n\n"
        f"You have access to the following tools:\n"
        f"{tool_text}\n\n"
        f"To use a tool, reply with: TOOL: tool_name(arguments)\n"
        f"If you cannot answer the task directly and do not have a tool, reply exactly:\n"
        f"\"I don't have a tool for handling {task_name}\".\n"
        f"Write the result of your attempt below your plan."
    )

    client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

async def process_task(engine, task_id: str):
    async with AsyncSession(engine, expire_on_commit=False) as session:
        result = await session.exec(select(Task).where(Task.id == task_id))
        task = result.first()
        if not task:
            print(f"Task {task_id} not found.")
            return
        print(f"Processing task: {task.id} - {task.name}")
        task.status = "in_progress"
        task.updated_at = datetime.utcnow()
        session.add(task)
        await session.commit()

        # Agentic behavior
        llm_result = await call_llm(task.name)
        print("LLM Response:\n" + llm_result)

        tool_pattern = r"TOOL: (\w+)\((.*?)\)"
        match = re.search(tool_pattern, llm_result)
        if match:
            tool_name, raw_args = match.group(1), match.group(2)
            tool_entry = get_registered_tool(tool_name)
            if tool_entry:
                func, _ = tool_entry
                try:
                    args = [arg.strip().strip("'\"") for arg in raw_args.split(",")]
                    tool_output = func(*args)
                    llm_result += f"\n\n[Tool {tool_name} output:]\n{tool_output}"
                except Exception as e:
                    llm_result += f"\n\n[Tool {tool_name} failed: {e}]"
            else:
                llm_result = f"I don't have a tool for handling {task.name}"
        else:
            refusal_phrases = [
                "i'm sorry", "i am not able", "i cannot", "as an ai",
                "i do not have the ability", "i can't", "i do not have access",
                "i am unable", "i don't have access"
            ]
            if not llm_result.strip() or any(phrase in llm_result.lower() for phrase in refusal_phrases):
                llm_result = f"I don't have a tool for handling {task.name}"

        task.status = "completed"
        task.result = llm_result
        task.updated_at = datetime.utcnow()
        session.add(task)
        await session.commit()
        print(f"Completed task: {task.id} - {task.name}")

async def agentic_worker():
    print("Starting agentic worker (single run)...")
    engine = get_engine()
    await init_db(engine)
    try:
        async with AsyncSession(engine, expire_on_commit=False) as session:
            result = await session.exec(select(Task).where(Task.status == "pending").limit(1))
            task = result.first()
        if task:
            await process_task(engine, task.id)
        else:
            print("No pending tasks found.")
    except Exception as e:
        print(f"Exception in worker: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print_registered_tools()
    asyncio.run(agentic_worker())
