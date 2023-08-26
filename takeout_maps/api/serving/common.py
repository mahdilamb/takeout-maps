import abc
import datetime
from typing import Any, Generic, Literal, Sequence, TypeVar

import pydantic

from takeout_maps.api.takeout import semantic_location_history

ErrorIDs = Literal["date-out-of-range"]

T = TypeVar("T", bound=pydantic.BaseModel)
S = TypeVar(
    "S",
    pydantic.BaseModel,
    dict[str, Any],
)


class Event(pydantic.BaseModel, abc.ABC):
    type: semantic_location_history.ActivityType | None
    id: int | None


class Location(pydantic.BaseModel):
    latitude: float
    longitude: float
    altitude: int | None = None
    accuracy: int | None = None
    timestamp: datetime.datetime


class Histories(pydantic.BaseModel):
    months: tuple[tuple[int, int], ...]


class Categorical(pydantic.BaseModel):
    color_map: dict[str, str]


class Linear(pydantic.BaseModel):
    dmin: float | str | None = None
    dmax: float | str | None = None
    min: str | None
    max: str | None


class Layer(pydantic.BaseModel):
    label: str
    path: str
    group_by: str | None = None
    color_by: str | None = None
    color_map: Categorical | Linear | Sequence[Linear] | None = None
    color: str


class Connection(pydantic.BaseModel):
    name: str
    path: str
    icon: str | None
    url: pydantic.AnyUrl | str | None
    connected: bool | None
    layers: Sequence[Layer]


class Dataset(pydantic.BaseModel, Generic[T, S]):
    metadata: S = pydantic.Field(default_factory=dict)
    data: Sequence[T]
    start: datetime.datetime | None = None
    end: datetime.datetime | None = None


class ExceptionDetail(pydantic.BaseModel, extra="allow"):
    errorMessage: str
    errorID: ErrorIDs


class LocationData(pydantic.BaseModel):
    locations: Sequence[Location]
    start: datetime.date
    end: datetime.date
