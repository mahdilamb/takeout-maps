import datetime
from typing import Literal, Sequence

import pydantic


class DeviceSpec(pydantic.BaseModel):
    manufacturer: str
    brand: str
    product: str
    device: str
    model: str
    is_low_ram: bool = pydantic.Field(alias="isLowRam")


class DeviceSettings(pydantic.BaseModel):
    device_tag: int = pydantic.Field(alias="deviceTag")
    reporting_enabled: bool = pydantic.Field(alias="reportingEnabled")
    device_pretty_name: str = pydantic.Field(alias="devicePrettyName")
    platform_type: str = pydantic.Field(alias="platformType")
    device_creation_time: datetime.datetime = pydantic.Field(alias="deviceCreationTime")
    latest_location_reporting_setting_change: dict[
        Literal["reportingEnabledModificationTime"], datetime.datetime
    ] = pydantic.Field(alias="latestLocationReportingSettingChange")
    android_os_level: int = pydantic.Field(alias="androidOsLevel")


class Settings(pydantic.BaseModel):
    created_time: datetime.datetime = pydantic.Field(alias="createdTime")
    modified_time: datetime.datetime = pydantic.Field(alias="modifiedTime")
    history_enabled: bool = pydantic.Field(alias="historyEnabled")
    history_deletion_time: datetime.datetime = pydantic.Field(
        alias="historyDeletionTime"
    )
    device_settings: Sequence[DeviceSettings] = pydantic.Field(alias="deviceSettings")
    retention_window_days: int = pydantic.Field(alias="retentionWindowDays")
    has_reported_locations: bool = pydantic.Field(alias="hasReportedLocations")
    has_set_retention: bool = pydantic.Field(alias="hasSetRetention")
