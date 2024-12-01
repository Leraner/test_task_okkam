from click import group
from sqlalchemy.ext.asyncio import AsyncSession
from database.schemas import CreateRespondentModelSchema
from database.models import RespondentModel
from database.exceptions import DatabaseException
from sqlalchemy import select, text, func, Float, cast


class RespondentDAL:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_precent(
        self, audience1: str | None = None, audience2: str | None = None
    ) -> float:

        groups = []

        for index, filter_ in enumerate([audience1, audience2]):
            query = select(
                RespondentModel.respondent,
                func.avg(RespondentModel.weight).label(f"group_{index}_weight"),
            ).group_by(RespondentModel.respondent)

            if filter_ is not None:
                query = query.where(text(filter_))

            groups.append(query.cte(f"group_{index}"))

        result_query = (
            select(
                cast(func.count(groups[1].c.respondent), Float)
                / cast(func.count(groups[0].c.respondent), Float)
            )
            .select_from(groups[0])
            .join(
                groups[1],
                groups[1].c.respondent == groups[0].c.respondent,
                isouter=True,
            )
        )

        result = await self.db_session.execute(result_query)

        rows = result.scalar()

        if rows is not None:
            return float(rows)
        
        raise DatabaseException(message="Результат не был получен")

    async def insert_database_dump(self, instances: list[CreateRespondentModelSchema]):
        models = [RespondentModel(**instance.model_dump()) for instance in instances]
        self.db_session.add_all(models)
        await self.db_session.commit()
