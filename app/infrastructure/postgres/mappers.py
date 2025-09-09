from abc import ABC
from abc import abstractmethod

from app.domain.models import BaseEntity
from app.domain.models import Task
from app.domain.models import User
from app.infrastructure.postgres.tables import BaseTable
from app.infrastructure.postgres.tables import TaskTable
from app.infrastructure.postgres.tables import UserTable


class BaseMapper(ABC):
    @abstractmethod
    async def to_entity(self, table_entity: BaseTable) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    async def to_table(self, entity: BaseEntity) -> BaseTable:
        raise NotImplementedError()


class TaskMapper(BaseMapper):
    async def to_entity(self, table_entity: TaskTable) -> Task:
        return Task(
            id=table_entity.id,
            created_at=table_entity.created_at,
            updated_at=table_entity.updated_at,
            title=table_entity.title,
            description=table_entity.description,
            user_id=table_entity.user_id,
            status=table_entity.status,
        )

    async def to_table(self, entity: Task) -> TaskTable:
        return TaskTable(
            **entity.model_dump(exclude={"status"}), status=entity.status.value
        )


class UserMapper(BaseMapper):
    async def to_entity(self, table_entity: UserTable) -> User:
        return User(
            id=table_entity.id,
            created_at=table_entity.created_at,
            updated_at=table_entity.updated_at,
            username=table_entity.username,
            hashed_password=table_entity.hashed_password,
        )

    async def to_table(self, entity: User) -> UserTable:
        return UserTable(**entity.model_dump())
