from abc import ABC
from abc import abstractmethod

from app.domain.models import BaseEntity
from app.domain.filters import BaseFilter


class IBaseRepository(ABC):
    @abstractmethod
    async def create(self, entity: BaseEntity) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    async def list(Self, filter_schema: BaseFilter) -> list[BaseEntity]:
        raise NotImplementedError()


class ITaskRepository(IBaseRepository):
    pass
