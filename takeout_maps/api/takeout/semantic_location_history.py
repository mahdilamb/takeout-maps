import datetime
from typing import Annotated, Any, Literal, Optional, TypeAlias, TypeVar

import pydantic
from git import Sequence


def falsy_to_none(x: Any) -> Any:
    return x or None


T = TypeVar("T")
EditConfirmationStatus: TypeAlias = Literal["CONFIRMED", "NOT_CONFIRMED"]
Confidence: TypeAlias = Literal["LOW", "MEDIUM", "HIGH", "UNKNOWN_CONFIDENCE"]
SemanticType: TypeAlias = Literal[
    "TYPE_ALIASED_LOCATION", "TYPE_HOME", "TYPE_SEARCHED_ADDRESS", "TYPE_WORK"
]
ActivityType: TypeAlias = Literal[
    "BOATING",
    "CATCHING_POKEMON",
    "CYCLING",
    "FLYING",
    "HIKING",
    "HORSEBACK_RIDING",
    "IN_BUS",
    "IN_CABLECAR",
    "IN_FERRY",
    "IN_FUNICULAR",
    "IN_GONDOLA_LIFT",
    "IN_PASSENGER_VEHICLE",
    "IN_SUBWAY",
    "IN_TAXI",
    "IN_TRAIN",
    "IN_TRAM",
    "IN_VEHICLE",
    "IN_WHEELCHAIR",
    "KAYAKING",
    "KITESURFING",
    "MOTORCYCLING",
    "PARAGLIDING",
    "ROWING",
    "RUNNING",
    "SAILING",
    "SKATEBOARDING",
    "SKATING",
    "SKIING",
    "SLEDDING",
    "SNOWBOARDING",
    "SNOWMOBILE",
    "SNOWSHOEING",
    "STILL",
    "SURFING",
    "SWIMMING",
    "UNKNOWN_ACTIVITY_TYPE",
    "WALKING",
    "WALKING_NORDIC",
]


class SourceInfo(pydantic.BaseModel):
    device_tag: int = pydantic.Field(alias="deviceTag")


class UIConfiguration(pydantic.BaseModel):
    ui_activity_segment_configuration: str | None = pydantic.Field(
        alias="uiPlaceVisitConfiguration", default=None
    )
    ui_activity_segment_configuration: str | None = pydantic.Field(
        alias="uiPlaceVisitConfiguration", default=None
    )


class Android(pydantic.BaseModel):
    fingerprint: str


class Device(pydantic.BaseModel):
    android: Android


class LatestKnownLocation(pydantic.BaseModel):
    detection_time: datetime.datetime = pydantic.Field(alias="detectionTime")
    location: "Location"


class Checkin(pydantic.BaseModel):
    at_time: datetime.datetime = pydantic.Field(alias="atTime")
    device: Device
    latest_known_location: LatestKnownLocation | None = pydantic.Field(
        alias="latestKnownLocation", default=None
    )


class PlaceVisitSegment(pydantic.BaseModel):
    location: Optional["Location"] = None


class OriginalCandidates(pydantic.BaseModel):
    place_visit_segment: PlaceVisitSegment = pydantic.Field(alias="placeVisitSegment")


class EditEvent(pydantic.BaseModel):
    edit_operaiton: Sequence[str] = pydantic.Field(alias="editOperation")
    ui_configuration: UIConfiguration | None = pydantic.Field(
        alias="uiConfiguration", default=None
    )


class EditHistory(pydantic.BaseModel):
    edit_event: Sequence[EditEvent] = pydantic.Field(alias="editEvent")


class EditActionMetadata(pydantic.BaseModel):
    activity_segment: Optional["ActivitySegment"] = pydantic.Field(
        alias="activitySegment", default=None
    )
    edit_history: EditHistory | None = pydantic.Field(alias="editHistory", default=None)
    original_candidates: OriginalCandidates | None = pydantic.Field(
        alias="originalCandidates", default=None
    )
    place_visit_segment: PlaceVisitSegment | None = pydantic.Field(
        alias="placeVisitSegment", default=None
    )


class Duration(pydantic.BaseModel):
    start_timestamp: datetime.datetime = pydantic.Field(alias="startTimestamp")
    end_timestamp: datetime.datetime = pydantic.Field(alias="endTimestamp")


class Location(pydantic.BaseModel):
    latitude_e7: float | None = pydantic.Field(alias="latitudeE7", default=None)
    longitude_e7: float | None = pydantic.Field(alias="longitudeE7", default=None)
    place_id: str | None = pydantic.Field(alias="placeId", default=None)
    address: str | None = None
    name: str | None = None
    semantic_type: SemanticType | None = pydantic.Field(
        default=None, alias="semanticType"
    )
    location_confidence: float = pydantic.Field(
        default=None, alias="locationConfidence"
    )
    accuracy_metres: int | None = pydantic.Field(alias="accuracyMetres", default=None)
    calibrated_probability: float | None = pydantic.Field(
        alias="calibratedProbability", default=None
    )
    is_current_location: bool | None = pydantic.Field(
        alias="isCurrentLocation", default=None
    )
    source_info: SourceInfo | None = pydantic.Field(alias="sourceInfo", default=None)


class Point(pydantic.BaseModel):
    lat_e7: float = pydantic.Field(alias="latE7")
    lng_e7: float = pydantic.Field(alias="lngE7")
    accuracy_metres: int | None = pydantic.Field(alias="accuracyMetres", default=None)
    timestamp: datetime.datetime = pydantic.Field(alias="timestamp")


class SimplifiedRawPath(pydantic.BaseModel):
    distance_meters: float | None = pydantic.Field(alias="distanceMeters", default=None)
    points: Sequence[Point]
    source: Literal["BACKFILLED", "INFERRED", "RESNAPPED_FOR_EDIT"] | None = None


class PlaceVisit(pydantic.BaseModel):
    location: Location
    duration: Duration | None = None
    place_confidence: str | None = pydantic.Field(alias="placeConfidence", default=None)
    center_lat_e7: float | None = pydantic.Field(alias="centerLatE7", default=None)
    center_lng_e7: float | None = pydantic.Field(alias="centerLngE7", default=None)
    visit_confidence: int | None = pydantic.Field(alias="visitConfidence", default=None)
    other_candidate_locations: Sequence[Location] | None = pydantic.Field(
        alias="otherCandidateLocations", default=None
    )
    edit_confirmation_status: EditConfirmationStatus = pydantic.Field(
        alias="editConfirmationStatus"
    )
    location_confidence: int | None = pydantic.Field(
        alias="locationConfidence", default=None
    )
    place_visit_type: str | None = pydantic.Field(alias="placeVisitType", default=None)
    place_visit_importance: Literal["MAIN", "TRANSITIONAL"] | None = pydantic.Field(
        alias="placeVisitImportance", default=None
    )
    child_visits: Sequence["PlaceVisit"] | None = pydantic.Field(
        alias="childVisits", default=None
    )
    place_visit_level: int | None = pydantic.Field(
        alias="plaeVisityLevel", default=None
    )
    section_id: str | None = pydantic.Field(alias="sectionId", default=None)
    simplified_raw_path: SimplifiedRawPath | None = pydantic.Field(
        alias="simplifiedRawPath", default=None
    )
    checkin: Checkin | None = None
    edit_action_metadata: EditActionMetadata | None = pydantic.Field(
        alias="editActionMetadata", default=None
    )


class Activity(pydantic.BaseModel):
    activity_type: ActivityType = pydantic.Field(alias="activityType")
    probability: float


class WayPoint(pydantic.BaseModel):
    lat_e7: float = pydantic.Field(alias="latE7")
    lng_e7: float = pydantic.Field(alias="lngE7")


class RoadSegment(pydantic.BaseModel):
    duration: str | None = None
    place_id: str = pydantic.Field(alias="placeId")


class WaypointPath(pydantic.BaseModel):
    waypoints: Sequence[WayPoint]
    source: str
    distance_meters: float | None = pydantic.Field(alias="distanceMeters", default=None)
    travel_mode: str | None = pydantic.Field(alias="travelMode", default=None)
    confidence: float | None = None
    road_segment: Sequence[RoadSegment] | None = pydantic.Field(
        alias="roadSegment", default=None
    )


class StopTimeInfo(pydantic.BaseModel):
    realtime_arrival_timestamp: datetime.datetime | None = pydantic.Field(
        alias="realtimeArrivalTimestamp", default=None
    )
    realtime_departure_timestamp: datetime.datetime | None = pydantic.Field(
        alias="realtimeDepartureTimestamp", default=None
    )
    schedule_arrival_timestamp: datetime.datetime | None = pydantic.Field(
        alias="scheduleArrivalTimestamp", default=None
    )
    scheduled_departure_timestamp: datetime.datetime | None = pydantic.Field(
        alias="scheduledDepartureTimestamp", default=None
    )


class TransitPath(pydantic.BaseModel):
    confidence: float | None = None
    distance_meters: float | None = pydantic.Field(alias="distanceMeters", default=None)
    hex_rgb_color: str = pydantic.Field(alias="hexRgbColor", pattern=r"[A-Fa-f0-9]{6}")
    line_place_id: str | None = pydantic.Field(alias="linePlaceId", default=None)
    name: str
    source: str
    stop_times_info: Sequence[StopTimeInfo] | None = pydantic.Field(
        alias="stopTimesInfo", default=None
    )
    transit_stops: Sequence[Location] = pydantic.Field(alias="transitStops")


class ParkingEvent(pydantic.BaseModel):
    location: Location
    location_source: str = pydantic.Field(alias="locationSource")
    method: str
    timestamp: datetime.datetime


class ActivitySegment(pydantic.BaseModel):
    start_location: Annotated[
        Location | None, pydantic.BeforeValidator(falsy_to_none)
    ] = pydantic.Field(default=None, alias="startLocation")
    end_location: Annotated[
        Location | None, pydantic.BeforeValidator(falsy_to_none)
    ] = pydantic.Field(default=None, alias="endLocation")
    duration: Duration | None = None
    distance: int | None = None
    confidence: Confidence | None = None
    activities: Sequence[Activity] | None = None
    activity_type: ActivityType | None = pydantic.Field(
        alias="activityType", default=None
    )
    waypoint_path: WaypointPath | None = pydantic.Field(
        alias="waypointPath", default=None
    )
    transit_path: TransitPath | None = pydantic.Field(alias="transitPath", default=None)
    parking_event: ParkingEvent | None = pydantic.Field(
        alias="parkingEvent", default=None
    )
    simplified_raw_path: SimplifiedRawPath | None = pydantic.Field(
        alias="simplifiedRawPath", default=None
    )
    edit_confirmation_status: EditConfirmationStatus | None = pydantic.Field(
        alias="editConfirmationStatus", default=None
    )
    edit_action_metadata: EditActionMetadata | None = pydantic.Field(
        alias="editActionMetadata", default=None
    )
    last_edited_timestamp: datetime.datetime | None = pydantic.Field(
        alias="lastEditedTimestamp", default=None
    )


class TimelineObject(pydantic.BaseModel):
    place_visit: PlaceVisit | None = pydantic.Field(alias="placeVisit", default=None)
    activity_segment: ActivitySegment | None = pydantic.Field(
        alias="activitySegment", default=None
    )


class SemanticLocationHistory(pydantic.BaseModel):
    timeline_objects: Sequence[TimelineObject] = pydantic.Field(alias="timelineObjects")
