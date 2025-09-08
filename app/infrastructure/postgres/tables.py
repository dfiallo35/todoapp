from uuid import uuid4

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


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
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    user = relationship("UserTable", back_populates="tasks")


class UserTable(BaseTable):
    __tablename__ = "user"

    username = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)

    tasks = relationship(
        "TaskTable", back_populates="user", cascade="all, delete-orphan"
    )
