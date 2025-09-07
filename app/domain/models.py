from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class BaseEntity(BaseModel):
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Task(BaseEntity):
    title: str
    description: str | None = None
