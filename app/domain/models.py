from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class BaseEntity(BaseModel):
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BaseUpdateSchema(BaseModel):
    pass


class Task(BaseEntity):
    title: str
    description: str | None = None


class TaskUpdateSchema(BaseUpdateSchema):
    title: str | None = None
    description: str | None = None
