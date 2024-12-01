from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel, field_validator
import datetime


class PrecentModelSchema(BaseModel):
    precent: float

    @field_validator('precent')
    @classmethod
    def validate_precent(cls, value):
        return round(value, 1)


class CreateRespondentModelSchema(BaseModel):
    id: int
    date: datetime.datetime
    respondent: int
    sex: int
    age: int
    weight: float