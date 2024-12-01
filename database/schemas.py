import datetime

from pydantic import BaseModel, field_validator


class PercentModelSchema(BaseModel):
    percent: float

    @field_validator('percent')
    @classmethod
    def validate_percent(cls, value):
        return round(value, 1)


class CreateRespondentModelSchema(BaseModel):
    id: int
    date: datetime.datetime
    respondent: int
    sex: int
    age: int
    weight: float
