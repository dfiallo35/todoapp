from fastapi import APIRouter
from fastapi import Query
from typing import Annotated

from app.presentation.serializers import TaskInput
from app.application.services import TaskCreateService
from app.application.services import TaskListService
from app.presentation.serializers import TaskMapper
from app.domain.filters import TaskFilter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/tasks")
async def create_task(
    task_input: TaskInput,
):
    mapper = TaskMapper()
    task_service = TaskCreateService()

    task = await mapper.to_entity(task_input)
    task = await task_service(task)
    return await mapper.to_api(task)


@router.get("/tasks")
async def list_task(
    filter_schema: Annotated[TaskFilter, Query()],
):
    mapper = TaskMapper()
    task_service = TaskListService()

    tasks = await task_service(filter_schema)
    return [await mapper.to_api(Task) for Task in tasks]
