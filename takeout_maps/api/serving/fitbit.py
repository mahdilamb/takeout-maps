import datetime
from typing import Generic, Literal, TypeVar

import pydantic

T = TypeVar("T", int, float)


class Steps(pydantic.BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    value: int


class Heartrate(pydantic.BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    value: int


class MinMax(pydantic.BaseModel, Generic[T]):
    min: T
    max: T


class HeartrateMetadata(pydantic.BaseModel):
    zones: dict[Literal["out_of_range", "fat_burn", "cardio", "peak"], MinMax[int]]
