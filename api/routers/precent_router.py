import sqlalchemy

from api.base.base_router import RegisterRoutes
from database.db import Database


class PercentRouter(RegisterRoutes):
    prefix = ""
    tags = ["percent"]

    database: Database

    @classmethod
    async def get_GetPercent(
        cls, audience1: str | None = None, audience2: str | None = None
    ):
        try:
            result = await cls.database.get_percent(
                audience1=audience1, audience2=audience2
            )
        except sqlalchemy.exc.DBAPIError:
            return {"error": "Введен неправильный фильтр"}
        return result

    @classmethod
    async def get_ping(cls):
        return {"success": True}
