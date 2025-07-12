# app/models/task.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Task(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
