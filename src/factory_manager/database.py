from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from . import config

settings = config.get_settings()


engine = create_async_engine(settings.database_url, echo=True)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


class SessionManager:
    def __init__(self) -> None:
        self.session: AsyncSession | None = None
        self.session_factory = async_scoped_session(
            async_session_maker, scopefunc=current_task
        )

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

    async def __aexit__(self, *args: object) -> None:
        await self.rollback()

    async def commit(self) -> None:
        if self.session:
            await self.session.commit()
            await self.session.close()
        self.session = None

    async def rollback(self) -> None:
        if self.session:
            await self.session.rollback()
            await self.session.close()
        self.session = None


session_manager = SessionManager()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager:
        session = session_manager.session
        if session is None:
            raise Exception("SessionManager is not initialized")
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
