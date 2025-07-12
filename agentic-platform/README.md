# Agentic Platform

## Overview

Agentic Platform is a modular, agentic task-processing system that combines a FastAPI backend for task management with an asynchronous worker that processes tasks using LLMs (OpenAI) and a flexible tool registry. The platform is designed for extensibility, security, and agentic reasoning, allowing the agent to use tools or answer directly based on the task.

---

## Features

- **FastAPI Backend**: Accepts and manages tasks via REST API.
- **Async Worker**: Processes tasks from a PostgreSQL database asynchronously.
- **Agentic Reasoning**: Uses OpenAI LLMs to interpret, plan, and attempt tasks.
- **Tool Registry**: Dynamically registers and invokes tools (e.g., web summarization, bank account mock).
- **Secure Secret Management**: API keys and secrets are loaded from files, not committed to git.
- **Extensible**: Easily add new tools for the agent to use.

---

## Architecture

```
+-------------------+      +-------------------+      +-------------------+
|   FastAPI API     | <--> |   PostgreSQL DB   | <--> |  Agentic Worker   |
+-------------------+      +-------------------+      +-------------------+
                                                        |
                                                        v
                                                +-------------------+
                                                |   Tool Registry   |
                                                +-------------------+
```

- **api/**: FastAPI app, schemas, and services
- **worker/**: Agentic worker, tool registry, and tools
- **shared/**: Shared config, models, and DB logic

---

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/agentic-platform.git
cd agentic-platform
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Set up the database

- Ensure PostgreSQL is running and accessible.
- Configure your DB connection in `shared/db/db.py` or via environment variables.

### 4. Add your OpenAI API key

- Create a file named `openai_api_key.secret` in the project root (next to `shared/`, `api/`, etc.).
- Paste your OpenAI API key into this file (no quotes, no spaces).
- **Do not commit this file to git!** It is already in `.gitignore`.

### 5. Run the API server

```sh
cd api
uvicorn main:app --reload
```

### 6. Run the agentic worker

```sh
cd ..
python worker/agentic_worker.py
```

Or for the MCP version:

```sh
python worker/agentic_worker_mcp.py
```

---

## Usage

- Submit tasks via the FastAPI endpoints (see `api/routes.py`).
- The worker will process pending tasks, call the LLM, and use tools if appropriate.
- Results are stored in the database and can be retrieved via the API.

---

## Tool Registry & Adding Tools

Tools are registered in `worker/tools/registry.py` and imported in the worker. To add a new tool:

1. Create a new Python file in `worker/tools/` (e.g., `my_tool.py`).
2. Define your tool function.
3. Register it using the `register_tool` function in `registry.py`.
4. Import your tool in the worker to ensure registration.

**Example:**

```python
# worker/tools/my_tool.py
from worker.tools.registry import register_tool

def my_tool(arg1):
    # Your logic here
    return f"Processed {arg1}"

register_tool(
    "my_tool",
    my_tool,
    "Description of what my_tool does. Usage: my_tool(arg1)"
)
```

---

## Security Best Practices

- **Never commit secrets** (API keys, passwords) to git.
- Store secrets in files like `openai_api_key.secret` and add them to `.gitignore`.
- If a secret is ever committed, remove it from git history and revoke it immediately.

---

## License

MIT License
