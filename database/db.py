from sqlalchemy.ext.asyncio import AsyncSession
from .dals import RespondentDAL
from .db_conn import DatabaseConnection
from .schemas import CreateRespondentModelSchema, PercentModelSchema
from .utils import SingletonMeta


class Database(metaclass=SingletonMeta):
    @DatabaseConnection.create_session
    async def get_percent(
            self,
            db_session: AsyncSession,
            audience1: str | None = None,
            audience2: str | None = None,
    ) -> PercentModelSchema:
        respondent_dal = RespondentDAL(db_session=db_session)
        percent = await respondent_dal.get_percent(
            audience1=audience1, audience2=audience2
        )
        return PercentModelSchema(percent=percent)

    @DatabaseConnection.create_session
    async def check_table_empty(self, db_session: AsyncSession) -> bool:
        respondent_dal = RespondentDAL(db_session=db_session)
        return await respondent_dal.check_on_empty()

    @DatabaseConnection.create_session
    async def insert_database_data(
            self, instances: list[CreateRespondentModelSchema], db_session: AsyncSession
    ) -> None:
        respondent_dal = RespondentDAL(db_session=db_session)
        await respondent_dal.insert_database_dump(instances=instances)
