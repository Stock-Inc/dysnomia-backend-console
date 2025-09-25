from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import sqlalchemy.exc as sqlalchemy_exc

from src.config import app_config

class DBSession:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url, echo=echo)

        self.db_session = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    @asynccontextmanager
    async def __call__(self, *args, **kwargs) -> AsyncIterator[AsyncSession]:
        session: AsyncSession = self.db_session()

        try:
            yield session
        except sqlalchemy_exc.SQLAlchemyError as exc:
            await session.rollback()
            raise
        finally:
            await session.close()


db_session = DBSession(
    url=app_config.POSTGRES.url, echo=False
)