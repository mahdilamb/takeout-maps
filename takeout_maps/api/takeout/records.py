import datetime
from typing import Literal, NamedTuple, Sequence, TypeAlias, TypeVar

import pydantic

T = TypeVar("T")
PydanticModel: TypeAlias = TypeVar("PydanticModel", bound=type[pydantic.BaseModel])
ActivityType: TypeAlias = Literal[
    "EXITING_VEHICLE",
    "IN_VEHICLE",
    "IN_RAIL_VEHICLE",
    "IN_ROAD_VEHICLE",
    "IN_FOUR_WHEELER_VEHICLE",
    "IN_BUS",
    "IN_CAR",
    "IN_TWO_WHEELER_VEHICLE",
    "ON_BICYCLE",
    "ON_FOOT",
    "RUNNING",
    "WALKING",
    "STILL",
    "TILTING",
    "UNKNOWN",
]


class AccessPoint(pydantic.BaseModel):
    frequency_Mhz: int = pydantic.Field(alias="frequencyMhz")
    is_connected: bool = pydantic.Field(alias="isConnected")
    mac: str
    strength: int


class WifiScan(pydantic.BaseModel):
    access_points: Sequence[AccessPoint] = pydantic.Field(alias="accessPoints")


class ExtraActivityInformation(pydantic.BaseModel):
    int_val: int = pydantic.Field(alias="intVal")
    name: str
    type: str


class Activity(pydantic.BaseModel):
    confidence: int | None = None
    extra: ExtraActivityInformation | None = None
    type: ActivityType | None = None


class ActivityRecord(pydantic.BaseModel):
    activity: Sequence[Activity]
    timestamp: datetime.datetime


class LocationMetadata(pydantic.BaseModel):
    timestamp: datetime.datetime
    wifi_scan: WifiScan


class Location(pydantic.BaseModel):
    latitude_e7: int = pydantic.Field(alias="latitudeE7")
    longitude_e7: int = pydantic.Field(alias="longitudeE7")
    os_level: int | None = pydantic.Field(alias="osLevel", default=None)
    location_metadata: Sequence[LocationMetadata] | None = pydantic.Field(
        alias="locationMetadata", default=None
    )
    place_id: str | None = pydantic.Field(alias="placeId", default=None)
    platform_type: str | None = pydantic.Field(alias="platformType", default=None)
    server_timestamp: datetime.datetime | None = pydantic.Field(
        alias="serverTimestamp", default=None
    )
    timestamp: datetime.datetime
    velocity: int | None = None
    vertical_accuracy: int | None = pydantic.Field(
        alias="verticalAccuracy", default=None
    )

    source: str
    accuracy: int
    active_wifi_scan: WifiScan | None = pydantic.Field(
        alias="activeWifiScan", default=None
    )
    activity: Sequence[Activity] | None = None
    altitude: int | None = None
    battery_charging: bool | None = pydantic.Field(
        alias="batteryCharging", default=None
    )
    device_designation: Literal["PRIMARY", "UNKNOWN"] | str | None = pydantic.Field(
        alias="deviceDesignation", default=None
    )
    device_tag: int = pydantic.Field(alias="deviceTag")
    heading: int | None = None
    inferred_location: Sequence["Location"] | None = pydantic.Field(
        alias="inferredLocation", default=None
    )


class FileCursor(NamedTuple):
    file_path: str
    path: tuple[None | str | int, ...]

    def descend(self, path: str | int) -> "FileCursor":
        cursor = FileCursor(
            file_path=self.file_path,
            path=self.path + (path,),
        )
        return cursor


class Records(pydantic.BaseModel):
    locations: Sequence[Location]
