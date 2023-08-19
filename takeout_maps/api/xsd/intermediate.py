import datetime
from typing import TypeAlias

import pydantic

Degrees: TypeAlias = float
Meters: TypeAlias = float
BPM: TypeAlias = float | None


class Point(pydantic.BaseModel):
    latitude: Degrees
    longitude: Degrees
    altitude: Meters | None = None
    elevation: float | None = None


class Activity(pydantic.BaseModel):
    points: dict[datetime.datetime, Point]
    heartrate: dict[datetime.datetime, BPM] | None = None
