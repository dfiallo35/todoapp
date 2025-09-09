from fastapi import APIRouter
from fastapi import Query
from fastapi import Depends
from fastapi import Response
from fastapi import status
from fastapi.exceptions import HTTPException
from typing import Annotated

from app.presentation.serializers import TaskInput
from app.presentation.serializers import TaskOutput
from app.presentation.serializers import TaskUpdateInput
from app.application.services import TaskCreateService
from app.application.services import TaskDeleteService
from app.application.services import TaskListService
from app.application.services import TaskUpdateService
from app.presentation.serializers import TaskMapper
from app.domain.filters import TaskFilter
from app.presentation.security import get_current_user


task_router = APIRouter(prefix="/tasks")


@task_router.post("/", response_model=TaskOutput)
async def create_task(
    task_input: TaskInput, response: Response, user_id: str = Depends(get_current_user)
):
    mapper = TaskMapper()
    task_create_service = TaskCreateService()

    task = await mapper.to_entity(task_input, user_id)
    task = await task_create_service(task)

    response.status_code = status.HTTP_201_CREATED
    return await mapper.to_api(task)


@task_router.get("/", response_model=list[TaskOutput])
async def list_task(
    filter_schema: Annotated[TaskFilter, Query()],
    response: Response,
    user_id: str = Depends(get_current_user),
):
    mapper = TaskMapper()
    task_list_service = TaskListService()

    filter_schema.user_id_eq = user_id
    tasks = await task_list_service(filter_schema)

    response.status_code = status.HTTP_200_OK
    return [await mapper.to_api(Task) for Task in tasks]


@task_router.get("/{id}", response_model=TaskOutput)
async def get_task(
    id: str, response: Response, user_id: str = Depends(get_current_user)
):
    mapper = TaskMapper()
    task_service = TaskListService()

    tasks = await task_service(TaskFilter(entity_id_eq=id, user_id_eq=user_id))
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} not found"
        )
    task = tasks[0]

    response.status_code = status.HTTP_200_OK
    return await mapper.to_api(task)


@task_router.delete("/{id}")
async def delete_task(id: str, user_id: str = Depends(get_current_user)):
    task_list_service = TaskListService()
    task_delete_service = TaskDeleteService()

    tasks = await task_list_service(TaskFilter(entity_id_eq=id, user_id_eq=user_id))
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} not found"
        )
    task = tasks[0]
    await task_delete_service(task)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@task_router.put("/{id}", response_model=TaskOutput)
async def update_task(
    id: str,
    response: Response,
    task_update: TaskUpdateInput,
    user_id: str = Depends(get_current_user),
):
    mapper = TaskMapper()
    task_list_service = TaskListService()
    task_update_service = TaskUpdateService()

    entity_update = await mapper.to_update_entity(task_update)
    tasks = await task_list_service(TaskFilter(entity_id_eq=id, user_id_eq=user_id))
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} not found"
        )
    task = tasks[0]
    task = await task_update_service(task, entity_update)

    response.status_code = status.HTTP_200_OK
    return await mapper.to_api(task)
