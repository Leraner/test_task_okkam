import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from .dals import RespondentDAL
from .db_conn import DatabaseConnection
from .schemas import CreateRespondentModelSchema, PrecentModelSchema
from decimal import Decimal

class Database:
    @DatabaseConnection.create_session
    async def get_precent(self, db_session: AsyncSession, audience1: str | None = None, audience2: str | None = None):
        respondent_dal = RespondentDAL(db_session=db_session)
        precent = await respondent_dal.get_precent(audience1=audience1, audience2=audience2)
        return PrecentModelSchema(precent=precent)

    @DatabaseConnection.create_session
    async def insert_database_data(self, instances: list[CreateRespondentModelSchema], db_session: AsyncSession):
        respondent_dal = RespondentDAL(db_session=db_session)
        await respondent_dal.insert_database_dump(instances=instances)

