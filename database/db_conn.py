from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from collections.abc import Awaitable, Callable
import settings


class DatabaseConnection:
    """Class for connecting to database and creating session for handler"""

    async_engine = create_async_engine(settings.DB_URL, echo=False)
    async_session = async_sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )

    @classmethod
    def create_session(cls, func: Callable) -> Callable[..., Awaitable]:
        """
        Generator for creating a session
        and adding it to the parameters of the wrapped function
        """

        async def inner(*args, **kwargs):
            async with cls.async_session() as db_session:
                async with db_session.begin():
                    return await func(*args, **kwargs, db_session=db_session)

        return inner