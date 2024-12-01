from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import uuid
import datetime


class Base(DeclarativeBase): ...


class RespondentModel(Base):
    __tablename__ = 'respondents'
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    respondent: Mapped[int] = mapped_column(nullable=False)
    sex: Mapped[int] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
