from fastapi import APIRouter
from fastapi import Query
from typing import Annotated

from app.presentation.serializers import TaskInput
from app.presentation.serializers import TaskUpdateInput
from app.application.services import TaskCreateService
from app.application.services import TaskDeleteService
from app.application.services import TaskListService
from app.application.services import TaskUpdateService
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


@router.get("/tasks/{id}")
async def get_task(id: str):
    mapper = TaskMapper()
    task_service = TaskListService()

    tasks = await task_service(TaskFilter(entity_id_eq=id))
    if not tasks:
        raise ValueError(f"Task with id {id} not found")
    task = tasks[0]
    return await mapper.to_api(task)


@router.delete("/tasks/{id}")
async def delete_task(id: str):
    task_list_service = TaskListService()
    task_delete_service = TaskDeleteService()

    tasks = await task_list_service(TaskFilter(entity_id_eq=id))
    if not tasks:
        raise ValueError(f"Task with id {id} not found")
    task = tasks[0]
    await task_delete_service(task)
    return {"status": "ok"}


@router.put("/tasks/{id}")
async def update_task(id: str, task_update: TaskUpdateInput):
    mapper = TaskMapper()
    task_list_service = TaskListService()
    task_update_service = TaskUpdateService()

    entity_update = await mapper.to_update_entity(task_update)
    tasks = await task_list_service(TaskFilter(entity_id_eq=id))
    if not tasks:
        raise ValueError(f"Task with id {id} not found")
    task = tasks[0]
    task = await task_update_service(task, entity_update)
    return await mapper.to_api(task)
