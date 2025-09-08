from pydantic import BaseModel
from abc import ABC
from abc import abstractmethod

from app.domain.models import BaseEntity
from app.domain.models import Task
from app.domain.models import TaskUpdateSchema


class BaseInput(BaseModel):
    pass


class BaseOutput(BaseModel):
    pass


class BaseUpdateInput(BaseInput):
    pass


class TaskInput(BaseInput):
    title: str
    description: str | None = None


class TaskOutput(BaseOutput):
    title: str
    description: str | None = None


class TaskUpdateInput(BaseUpdateInput):
    title: str | None = None
    description: str | None = None


class BaseMapper(ABC):
    @abstractmethod
    async def to_entity(self, serilizer: BaseInput) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    async def to_api(self, entity: BaseEntity) -> BaseOutput:
        raise NotImplementedError()


class TaskMapper(BaseMapper):
    async def to_entity(self, serilizer: TaskInput, user_id: str) -> Task:
        return Task(**serilizer.model_dump(), user_id=user_id)

    async def to_api(self, entity: Task) -> TaskOutput:
        return TaskOutput(**entity.model_dump())

    async def to_update_entity(self, serilizer: TaskUpdateInput) -> TaskUpdateSchema:
        return TaskUpdateSchema(**serilizer.model_dump(exclude_unset=True))
