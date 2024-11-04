from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False
    )
    return pool


def create_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(
        url=database_url,
        poolclass=AsyncAdaptedQueuePool,
        pool_size=3,
        max_overflow=2,
        # echo=True,
    )
