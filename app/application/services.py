from abc import ABC
from abc import abstractmethod
import inject

from app.domain.models import BaseEntity
from app.domain.models import BaseUpdateSchema
from app.domain.models import Task
from app.domain.models import TaskUpdateSchema
from app.domain.repositories import IBaseRepository
from app.domain.repositories import ITaskRepository
from app.domain.filters import BaseFilter
from app.domain.filters import TaskFilter


class BaseService(ABC):
    repo_instance: IBaseRepository

    @abstractmethod
    async def execute(self, *args, **kwargs):
        raise NotImplementedError()

    async def __call__(self, *args, **kwds):
        return await self.execute(*args, **kwds)


class BaseListService(BaseService):
    async def execute(self, filter_schema: BaseFilter):
        return await self.repo_instance.list(filter_schema=filter_schema)


class BaseCreateService(BaseService):
    async def execute(self, entity: BaseEntity):
        return await self.repo_instance.create(entity=entity)


class BaseDeleteService(BaseService):
    async def execute(self, entity: BaseEntity):
        return await self.repo_instance.delete(entity=entity)


class BaseUpdateService(BaseService):
    async def execute(self, entity: BaseEntity, update_schema: BaseUpdateSchema):
        return await self.repo_instance.update(
            entity=entity, update_schema=update_schema
        )


class TaskListService(BaseListService):
    repo_instance: ITaskRepository = inject.attr(ITaskRepository)

    async def execute(self, filter_schema: TaskFilter):
        return await super().execute(filter_schema=filter_schema)


class TaskCreateService(BaseCreateService):
    repo_instance: ITaskRepository = inject.attr(ITaskRepository)

    async def execute(self, entity: Task):
        return await super().execute(entity=entity)


class TaskDeleteService(BaseDeleteService):
    repo_instance: ITaskRepository = inject.attr(ITaskRepository)

    async def execute(self, entity: Task):
        return await super().execute(entity=entity)


class TaskUpdateService(BaseUpdateService):
    repo_instance: ITaskRepository = inject.attr(ITaskRepository)

    async def execute(self, entity: Task, update_schema: TaskUpdateSchema):
        return await super().execute(entity=entity, update_schema=update_schema)
