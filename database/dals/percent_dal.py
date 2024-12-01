from sqlalchemy.ext.asyncio import AsyncSession
from database.schemas import CreateRespondentModelSchema
from database.models import RespondentModel
from sqlalchemy import select, text, func, Float, cast, and_, exists


class RespondentDAL:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_percent(
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

        intersection = (
            select(
                cast(
                    func.sum(groups[1].c.group_1_weight),
                    Float,
                )
                / cast(
                    func.sum(groups[0].c.group_0_weight),
                    Float,
                ),
            )
            .select_from(groups[0])
            .join(
                groups[1],
                and_(
                    groups[1].c.group_1_weight == groups[0].c.group_0_weight,
                    groups[1].c.respondent == groups[0].c.respondent,
                ),
                isouter=True,
            )
        )

        result = await self.db_session.execute(intersection)

        rows = result.scalar()

        if rows is not None:
            return float(rows)

        return 0

    async def check_on_empty(self) -> bool:
        query = select(exists(RespondentModel))

        result = await self.db_session.execute(query)
        return bool(result.scalar())

    async def insert_database_dump(self, instances: list[CreateRespondentModelSchema]) -> None:
        models = [RespondentModel(**instance.model_dump()) for instance in instances]
        self.db_session.add_all(models)
        await self.db_session.commit()
