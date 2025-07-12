# app/schemas/task.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    name: str

class TaskRead(BaseModel):
    id: str
    name: str
    status: str
    result: Optional[str]
    created_at: datetime
    updated_at: datetime
