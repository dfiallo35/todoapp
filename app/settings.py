import inject
from inject import Binder
from pydantic_settings import BaseSettings

from app.infrastructure.postgres.repositories import TaskRepository
from app.infrastructure.postgres.repositories import UserRepository
from app.domain.repositories import ITaskRepository
from app.domain.repositories import IUserRepository
from app.infrastructure.postgres.db import DbConnection


class Settings(BaseSettings):
    DEPENDENCIES: dict
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"

    db_connection: DbConnection | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def configure(self, binder: Binder):
        self.db_connection = DbConnection(self.DATABASE_URL)
        for interface, implementation in self.DEPENDENCIES.items():
            binder.bind(interface, implementation(self.db_connection))

    def setup(self):
        inject.configure(self.configure)


DEPENDENCIES = {
    ITaskRepository: TaskRepository,
    IUserRepository: UserRepository,
}

settings = Settings(DEPENDENCIES=DEPENDENCIES)
