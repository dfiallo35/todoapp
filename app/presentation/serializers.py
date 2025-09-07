from pydantic import BaseModel
from abc import ABC
from abc import abstractmethod

from app.domain.models import BaseEntity
from app.domain.models import Task


class BaseInput(BaseModel):
    pass


class BaseOutput(BaseModel):
    pass


class TaskInput(BaseInput):
    title: str
    description: str | None = None


class TaskOutput(BaseOutput):
    title: str
    description: str | None = None


class BaseMapper(ABC):
    @abstractmethod
    async def to_entity(self, serilizer: BaseInput) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    async def to_api(self, entity: BaseEntity) -> BaseOutput:
        raise NotImplementedError()


class TaskMapper(BaseMapper):
    async def to_entity(self, serilizer: TaskInput) -> Task:
        return Task(**serilizer.model_dump())

    async def to_api(self, entity: Task) -> TaskOutput:
        return TaskOutput(**entity.model_dump())
