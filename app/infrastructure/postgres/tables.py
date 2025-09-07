from uuid import uuid4

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
from sqlalchemy import func


class BaseTable(DeclarativeBase):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class TaskTable(BaseTable):
    __tablename__ = "task"

    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
