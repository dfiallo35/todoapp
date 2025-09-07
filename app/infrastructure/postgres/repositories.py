from sqlalchemy import select
from sqlalchemy.sql import Select

from app.infrastructure.postgres.db import DbConnection
from app.domain.repositories import IBaseRepository
from app.domain.repositories import ITaskRepository
from app.domain.models import BaseEntity
from app.domain.models import BaseUpdateSchema
from app.domain.filters import BaseFilter
from app.domain.filters import TaskFilter
from app.infrastructure.postgres.tables import BaseTable
from app.infrastructure.postgres.tables import TaskTable
from app.infrastructure.postgres.mappers import BaseMapper
from app.infrastructure.postgres.mappers import TaskMapper


class BaseRepository(IBaseRepository):
    table_class: BaseTable
    db_connection: DbConnection
    mapper_class: BaseMapper

    def __init__(self, db_connection: DbConnection):
        self.db_connection = db_connection

    async def filter(self, filter_schema: BaseFilter, query: Select) -> Select:
        if filter_schema.limit:
            query = query.limit(filter_schema.limit)
        if filter_schema.offset:
            query = query.offset(filter_schema.offset)
        if filter_schema.order_by:
            order_field = filter_schema.order_by
            desc = order_field.startswith("-")
            field_name = order_field.lstrip("-")

            column = getattr(self.table_class, field_name, None)
            if column is not None:
                query = query.order_by(column.desc() if desc else column.asc())
        return query

    async def create(self, entity: BaseEntity) -> BaseEntity:
        async with self.db_connection.get_session() as session:
            table_entity = await self.mapper_class().to_table(entity)
            session.add(table_entity)
            await session.commit()
            return await self.mapper_class().to_entity(table_entity)

    async def list(self, filter_schema: BaseFilter) -> list[BaseEntity]:
        async with self.db_connection.get_session() as session:
            query = await self.filter(
                filter_schema=filter_schema, query=select(self.table_class)
            )
            result = await session.execute(query)
            return [
                await self.mapper_class().to_entity(table_entity)
                for table_entity in result.scalars().all()
            ]

    async def delete(self, entity: BaseEntity) -> None:
        async with self.db_connection.get_session() as session:
            table_entity = await session.get(self.table_class, entity.id)
            if table_entity is None:
                return
            await session.delete(table_entity)
            await session.commit()

    async def update(
        self, entity: BaseEntity, update_schema: BaseUpdateSchema
    ) -> BaseEntity:
        async with self.db_connection.get_session() as session:
            table_entity = await session.get(self.table_class, entity.id)
            if table_entity is None:
                return

            for key, value in update_schema.model_dump(exclude_unset=True).items():
                setattr(table_entity, key, value)
            await session.commit()
            await session.refresh(table_entity)
            return await self.mapper_class().to_entity(table_entity)


class TaskRepository(ITaskRepository, BaseRepository):
    table_class: TaskTable = TaskTable
    mapper_class: TaskMapper = TaskMapper

    async def filter(self, filter_schema: TaskFilter, query: Select) -> Select:
        query = await super().filter(filter_schema, query)

        if filter_schema.entity_id_eq:
            query = query.where(self.table_class.id == filter_schema.entity_id_eq)

        return query
