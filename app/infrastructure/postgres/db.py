from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class DbConnection:
    def __init__(self, db_url: str):
        if not db_url:
            raise Exception("Database URL is required")

        self.engine = create_async_engine(db_url, echo=True, future=True)

        self.session_factory = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    def get_session(self) -> AsyncSession:
        return self.session_factory()
