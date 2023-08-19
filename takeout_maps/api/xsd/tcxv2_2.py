import abc
import datetime
import urllib.request
from typing import Annotated, Literal, Optional, Sequence, TypeAlias

import annotated_types
import pydantic
import xmltodict

import takeout_maps.xsds as xsds

Token_t: TypeAlias = Annotated[str, None]
CadenceValue_t: TypeAlias = Annotated[
    int, annotated_types.Ge(0), annotated_types.Lt(256), annotated_types.Le(254)
]
DegreesLongitude_t: TypeAlias = Annotated[float, annotated_types.Ge(-180.0)]
DegreesLatitude_t: TypeAlias = Annotated[
    float, annotated_types.Le(90.0), annotated_types.Ge(-90.0)
]
StepId_t: TypeAlias = Annotated[int, annotated_types.Gt(0), annotated_types.Le(20)]
Repetitions_t: TypeAlias = Annotated[
    int, annotated_types.Gt(0), annotated_types.Le(99), annotated_types.Ge(2)
]
SpeedZoneNumbers_t: TypeAlias = Annotated[
    int, annotated_types.Gt(0), annotated_types.Le(10)
]
SpeedInMetersPerSecond_t: TypeAlias = Annotated[float, None]
HeartRateZoneNumbers_t: TypeAlias = Annotated[
    int, annotated_types.Gt(0), annotated_types.Le(5)
]
PercentOfMax_t: TypeAlias = Annotated[
    int,
    annotated_types.Ge(0),
    annotated_types.Lt(256),
    annotated_types.Le(100),
    annotated_types.Ge(0),
]
positiveByte: TypeAlias = Annotated[
    int, annotated_types.Ge(0), annotated_types.Lt(256), annotated_types.Ge(1)
]
unsignedInt: TypeAlias = Annotated[
    int, annotated_types.Ge(0), annotated_types.Lt(4294967296)
]
unsignedShort: TypeAlias = Annotated[
    int, annotated_types.Ge(0), annotated_types.Lt(65536)
]
Sport_t: TypeAlias = Annotated[Literal["Running", "Biking", "Other"], None]
LangID_t: TypeAlias = Annotated[Token_t, pydantic.constr(min_length=2, max_length=2)]
PartNumber_t: TypeAlias = Annotated[
    Token_t, pydantic.constr(pattern=r"[\p{Lu}\d]{3}-[\p{Lu}\d]{5}-[\p{Lu}\d]{2}")
]
BuildType_t: TypeAlias = Annotated[
    Literal["Internal", "Alpha", "Beta", "Release"], None
]
TrainingType_t: TypeAlias = Annotated[Literal["Workout", "Course"], None]
TriggerMethod_t: TypeAlias = Annotated[
    Literal["Manual", "Distance", "Location", "Time", "HeartRate"], None
]
SensorState_t: TypeAlias = Annotated[Literal["Present", "Absent"], None]
RestrictedToken_t: TypeAlias = Annotated[
    Token_t, pydantic.constr(max_length=15), pydantic.constr(min_length=1)
]
Intensity_t: TypeAlias = Annotated[Literal["Active", "Resting"], None]
SpeedType_t: TypeAlias = Annotated[Literal["Pace", "Speed"], None]
Gender_t: TypeAlias = Annotated[Literal["Male", "Female"], None]
CoursePointName_t: TypeAlias = Annotated[
    Token_t, pydantic.constr(max_length=10), pydantic.constr(min_length=1)
]
CoursePointType_t: TypeAlias = Annotated[
    Literal[
        "Generic",
        "Summit",
        "Valley",
        "Water",
        "Food",
        "Danger",
        "Left",
        "Right",
        "Straight",
        "First Aid",
        "4th Category",
        "3rd Category",
        "2nd Category",
        "1st Category",
        "Hors Category",
        "Sprint",
    ],
    None,
]


class AbstractSource_t(pydantic.BaseModel, abc.ABC):
    name: Optional["Token_t"] = pydantic.Field(default=None, alias="Name")


class AbstractStep_t(pydantic.BaseModel, abc.ABC):
    step_id: Optional["StepId_t"] = pydantic.Field(default=None, alias="StepId")


class Duration_t(pydantic.BaseModel, abc.ABC):
    ...


class Target_t(pydantic.BaseModel, abc.ABC):
    ...


class HeartRateValue_t(pydantic.BaseModel, abc.ABC):
    ...


class Zone_t(pydantic.BaseModel, abc.ABC):
    ...


class TrainingCenterDatabase_t(pydantic.BaseModel):
    folders: Optional["Folders_t"] = pydantic.Field(default=None, alias="Folders")
    activities: Optional["ActivityList_t"] = pydantic.Field(
        default=None, alias="Activities"
    )
    workouts: Optional["WorkoutList_t"] = pydantic.Field(default=None, alias="Workouts")
    courses: Optional["CourseList_t"] = pydantic.Field(default=None, alias="Courses")
    author: Optional["AbstractSource_t"] = pydantic.Field(default=None, alias="Author")
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.


class Folders_t(pydantic.BaseModel):
    history: Optional["History_t"] = pydantic.Field(default=None, alias="History")
    workouts: Optional["Workouts_t"] = pydantic.Field(default=None, alias="Workouts")
    courses: Optional["Courses_t"] = pydantic.Field(default=None, alias="Courses")


class ActivityList_t(pydantic.BaseModel):
    activity: Sequence["Activity_t"] = pydantic.Field(
        default_factory=tuple, alias="Activity"
    )
    multi_sport_session: Sequence["MultiSportSession_t"] = pydantic.Field(
        default_factory=tuple, alias="MultiSportSession"
    )


class WorkoutList_t(pydantic.BaseModel):
    workout: Sequence["Workout_t"] = pydantic.Field(
        default_factory=tuple, alias="Workout"
    )  # The StepId should be unique within a workout and should notexceed 20. This restricts the number of steps in a workout to 20.


class CourseList_t(pydantic.BaseModel):
    course: Sequence["Course_t"] = pydantic.Field(default_factory=tuple, alias="Course")


class History_t(pydantic.BaseModel):
    running: Optional["HistoryFolder_t"] = pydantic.Field(default=None, alias="Running")
    biking: Optional["HistoryFolder_t"] = pydantic.Field(default=None, alias="Biking")
    other: Optional["HistoryFolder_t"] = pydantic.Field(default=None, alias="Other")
    multi_sport: Optional["MultiSportFolder_t"] = pydantic.Field(
        default=None, alias="MultiSport"
    )
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.


class ActivityReference_t(pydantic.BaseModel):
    id: datetime.datetime | None = pydantic.Field(default=None, alias="Id")


class HistoryFolder_t(pydantic.BaseModel):
    folder: Sequence["HistoryFolder_t"] = pydantic.Field(
        default_factory=tuple, alias="Folder"
    )
    activity_ref: Sequence[ActivityReference_t] = pydantic.Field(
        default_factory=tuple, alias="ActivityRef"
    )
    week: Sequence["Week_t"] = pydantic.Field(default_factory=tuple, alias="Week")
    notes: str | None = pydantic.Field(default=None, alias="Notes")
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.
    name: str = pydantic.Field(alias="@Name")


class MultiSportFolder_t(pydantic.BaseModel):
    folder: Sequence["MultiSportFolder_t"] = pydantic.Field(
        default_factory=tuple, alias="Folder"
    )
    multisport_activity_ref: Sequence[ActivityReference_t] = pydantic.Field(
        default_factory=tuple, alias="MultisportActivityRef"
    )
    week: Sequence["Week_t"] = pydantic.Field(default_factory=tuple, alias="Week")
    notes: str | None = pydantic.Field(default=None, alias="Notes")
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.
    name: str = pydantic.Field(alias="@Name")


class Week_t(pydantic.BaseModel):
    """The week is written out only if the notes are present."""

    notes: str | None = pydantic.Field(default=None, alias="Notes")
    start_day: datetime.date = pydantic.Field(alias="@StartDay")


class MultiSportSession_t(pydantic.BaseModel):
    id: datetime.datetime | None = pydantic.Field(default=None, alias="Id")
    first_sport: Optional["FirstSport_t"] = pydantic.Field(
        default=None, alias="FirstSport"
    )
    next_sport: Sequence["NextSport_t"] = pydantic.Field(
        default_factory=tuple, alias="NextSport"
    )
    notes: str | None = pydantic.Field(default=None, alias="Notes")


class FirstSport_t(pydantic.BaseModel):
    activity: Optional["Activity_t"] = pydantic.Field(default=None, alias="Activity")


class NextSport_t(pydantic.BaseModel):
    """Each sport contains an optional transition and a run."""

    transition: Optional["ActivityLap_t"] = pydantic.Field(
        default=None, alias="Transition"
    )
    activity: Optional["Activity_t"] = pydantic.Field(default=None, alias="Activity")


class Activity_t(pydantic.BaseModel):
    id: datetime.datetime | None = pydantic.Field(default=None, alias="Id")
    lap: Sequence["ActivityLap_t"] = pydantic.Field(default_factory=tuple, alias="Lap")
    notes: str | None = pydantic.Field(default=None, alias="Notes")
    training: Optional["Training_t"] = pydantic.Field(default=None, alias="Training")
    creator: Optional["AbstractSource_t"] = pydantic.Field(
        default=None, alias="Creator"
    )
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.
    sport: Sport_t = pydantic.Field(alias="@Sport")


class Device_t(AbstractSource_t):
    """Identifies the originating GPS device that tracked a run orused to identify the
    type of device capable of handlingthe data for loading."""

    unit_id: unsignedInt | None = pydantic.Field(default=None, alias="UnitId")
    product_i_d: unsignedShort | None = pydantic.Field(default=None, alias="ProductID")
    version: Optional["Version_t"] = pydantic.Field(default=None, alias="Version")


class Application_t(AbstractSource_t):
    """Identifies a PC software application."""

    build: Optional["Build_t"] = pydantic.Field(default=None, alias="Build")
    lang_i_d: Optional["LangID_t"] = pydantic.Field(default=None, alias="LangID")
    part_number: Optional["PartNumber_t"] = pydantic.Field(
        default=None, alias="PartNumber"
    )


class Build_t(pydantic.BaseModel):
    version: Optional["Version_t"] = pydantic.Field(default=None, alias="Version")
    type: Optional["BuildType_t"] = pydantic.Field(default=None, alias="Type")
    time: Optional["Token_t"] = pydantic.Field(
        default=None, alias="Time"
    )  # A string containing the date and time when an application was built.Note that this is not an xsd:dateTime type because this string isgenerated by the compiler and cannot be readily converted to thexsd:dateTime format.
    builder: Optional["Token_t"] = pydantic.Field(
        default=None, alias="Builder"
    )  # The login name of the engineer who created this build.


class Version_t(pydantic.BaseModel):
    version_major: unsignedShort | None = pydantic.Field(
        default=None, alias="VersionMajor"
    )
    version_minor: unsignedShort | None = pydantic.Field(
        default=None, alias="VersionMinor"
    )
    build_major: unsignedShort | None = pydantic.Field(default=None, alias="BuildMajor")
    build_minor: unsignedShort | None = pydantic.Field(default=None, alias="BuildMinor")


class Training_t(pydantic.BaseModel):
    quick_workout_results: Optional["QuickWorkout_t"] = pydantic.Field(
        default=None, alias="QuickWorkoutResults"
    )
    plan: Optional["Plan_t"] = pydantic.Field(default=None, alias="Plan")
    virtual_partner: bool = pydantic.Field(alias="@VirtualPartner")


class QuickWorkout_t(pydantic.BaseModel):
    total_time_seconds: float | None = pydantic.Field(
        default=None, alias="TotalTimeSeconds"
    )
    distance_meters: float | None = pydantic.Field(default=None, alias="DistanceMeters")


class Plan_t(pydantic.BaseModel):
    name: Optional["RestrictedToken_t"] = pydantic.Field(default=None, alias="Name")
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.
    type: TrainingType_t = pydantic.Field(alias="@Type")
    interval_workout: bool = pydantic.Field(alias="@IntervalWorkout")


class ActivityLap_t(pydantic.BaseModel):
    total_time_seconds: float | None = pydantic.Field(
        default=None, alias="TotalTimeSeconds"
    )
    distance_meters: float | None = pydantic.Field(default=None, alias="DistanceMeters")
    maximum_speed: float | None = pydantic.Field(default=None, alias="MaximumSpeed")
    calories: unsignedShort | None = pydantic.Field(default=None, alias="Calories")
    average_heart_rate_bpm: Optional["HeartRateInBeatsPerMinute_t"] = pydantic.Field(
        default=None, alias="AverageHeartRateBpm"
    )
    maximum_heart_rate_bpm: Optional["HeartRateInBeatsPerMinute_t"] = pydantic.Field(
        default=None, alias="MaximumHeartRateBpm"
    )
    intensity: Optional["Intensity_t"] = pydantic.Field(default=None, alias="Intensity")
    cadence: Optional["CadenceValue_t"] = pydantic.Field(default=None, alias="Cadence")
    trigger_method: Optional["TriggerMethod_t"] = pydantic.Field(
        default=None, alias="TriggerMethod"
    )
    track: Sequence["Track_t"] = pydantic.Field(default_factory=tuple, alias="Track")
    notes: str | None = pydantic.Field(default=None, alias="Notes")
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.
    start_time: datetime.datetime = pydantic.Field(alias="@StartTime")


class Track_t(pydantic.BaseModel):
    trackpoint: Sequence["Trackpoint_t"] = pydantic.Field(
        default_factory=tuple, alias="Trackpoint"
    )


class Trackpoint_t(pydantic.BaseModel):
    time: datetime.datetime | None = pydantic.Field(default=None, alias="Time")
    position: Optional["Position_t"] = pydantic.Field(default=None, alias="Position")
    altitude_meters: float | None = pydantic.Field(default=None, alias="AltitudeMeters")
    distance_meters: float | None = pydantic.Field(default=None, alias="DistanceMeters")
    heart_rate_bpm: Optional["HeartRateInBeatsPerMinute_t"] = pydantic.Field(
        default=None, alias="HeartRateBpm"
    )
    cadence: Optional["CadenceValue_t"] = pydantic.Field(default=None, alias="Cadence")
    sensor_state: Optional["SensorState_t"] = pydantic.Field(
        default=None, alias="SensorState"
    )
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.


class Position_t(pydantic.BaseModel):
    latitude_degrees: Optional["DegreesLatitude_t"] = pydantic.Field(
        default=None, alias="LatitudeDegrees"
    )
    longitude_degrees: Optional["DegreesLongitude_t"] = pydantic.Field(
        default=None, alias="LongitudeDegrees"
    )


class Workouts_t(pydantic.BaseModel):
    running: Optional["WorkoutFolder_t"] = pydantic.Field(default=None, alias="Running")
    biking: Optional["WorkoutFolder_t"] = pydantic.Field(default=None, alias="Biking")
    other: Optional["WorkoutFolder_t"] = pydantic.Field(default=None, alias="Other")
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.


class NameKeyReference_t(pydantic.BaseModel):
    id: Optional["RestrictedToken_t"] = pydantic.Field(default=None, alias="Id")


class WorkoutFolder_t(pydantic.BaseModel):
    folder: Sequence["WorkoutFolder_t"] = pydantic.Field(
        default_factory=tuple, alias="Folder"
    )
    workout_name_ref: Sequence[NameKeyReference_t] = pydantic.Field(
        default_factory=tuple, alias="WorkoutNameRef"
    )
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.
    name: str = pydantic.Field(alias="@Name")


class Workout_t(pydantic.BaseModel):
    name: Optional["RestrictedToken_t"] = pydantic.Field(default=None, alias="Name")
    step: Sequence["AbstractStep_t"] = pydantic.Field(
        default_factory=tuple, alias="Step"
    )
    scheduled_on: Sequence[datetime.date] = pydantic.Field(
        default_factory=tuple, alias="ScheduledOn"
    )
    notes: str | None = pydantic.Field(default=None, alias="Notes")
    creator: Optional["AbstractSource_t"] = pydantic.Field(
        default=None, alias="Creator"
    )
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.
    sport: Sport_t = pydantic.Field(alias="@Sport")


class Repeat_t(AbstractStep_t):
    repetitions: Optional["Repetitions_t"] = pydantic.Field(
        default=None, alias="Repetitions"
    )
    child: Sequence["AbstractStep_t"] = pydantic.Field(
        default_factory=tuple, alias="Child"
    )


class Step_t(AbstractStep_t):
    name: Optional["RestrictedToken_t"] = pydantic.Field(default=None, alias="Name")
    duration: Optional["Duration_t"] = pydantic.Field(default=None, alias="Duration")
    intensity: Optional["Intensity_t"] = pydantic.Field(default=None, alias="Intensity")
    target: Optional["Target_t"] = pydantic.Field(default=None, alias="Target")


class Time_t(Duration_t):
    seconds: unsignedShort | None = pydantic.Field(default=None, alias="Seconds")


class Distance_t(Duration_t):
    meters: unsignedShort | None = pydantic.Field(default=None, alias="Meters")


class HeartRateAbove_t(Duration_t):
    heart_rate: Optional["HeartRateValue_t"] = pydantic.Field(
        default=None, alias="HeartRate"
    )


class HeartRateBelow_t(Duration_t):
    heart_rate: Optional["HeartRateValue_t"] = pydantic.Field(
        default=None, alias="HeartRate"
    )


class CaloriesBurned_t(Duration_t):
    calories: unsignedShort | None = pydantic.Field(default=None, alias="Calories")


class UserInitiated_t(Duration_t):
    ...


class Speed_t(Target_t):
    speed_zone: Optional["Zone_t"] = pydantic.Field(default=None, alias="SpeedZone")


class HeartRate_t(Target_t):
    heart_rate_zone: Optional["Zone_t"] = pydantic.Field(
        default=None, alias="HeartRateZone"
    )


class Cadence_t(Target_t):
    low: float | None = pydantic.Field(default=None, alias="Low")
    high: float | None = pydantic.Field(default=None, alias="High")


class None_t(Target_t):
    ...


class PredefinedSpeedZone_t(Zone_t):
    number: Optional["SpeedZoneNumbers_t"] = pydantic.Field(
        default=None, alias="Number"
    )


class CustomSpeedZone_t(Zone_t):
    view_as: Optional["SpeedType_t"] = pydantic.Field(default=None, alias="ViewAs")
    low_in_meters_per_second: Optional["SpeedInMetersPerSecond_t"] = pydantic.Field(
        default=None, alias="LowInMetersPerSecond"
    )
    high_in_meters_per_second: Optional["SpeedInMetersPerSecond_t"] = pydantic.Field(
        default=None, alias="HighInMetersPerSecond"
    )


class PredefinedHeartRateZone_t(Zone_t):
    number: Optional["HeartRateZoneNumbers_t"] = pydantic.Field(
        default=None, alias="Number"
    )


class CustomHeartRateZone_t(Zone_t):
    low: Optional["HeartRateValue_t"] = pydantic.Field(default=None, alias="Low")
    high: Optional["HeartRateValue_t"] = pydantic.Field(default=None, alias="High")


class HeartRateInBeatsPerMinute_t(HeartRateValue_t):
    value: Optional["positiveByte"] = pydantic.Field(default=None, alias="Value")


class HeartRateAsPercentOfMax_t(HeartRateValue_t):
    value: Optional["PercentOfMax_t"] = pydantic.Field(default=None, alias="Value")


class Courses_t(pydantic.BaseModel):
    course_folder: Optional["CourseFolder_t"] = pydantic.Field(
        default=None, alias="CourseFolder"
    )
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.


class CourseFolder_t(pydantic.BaseModel):
    folder: Sequence["CourseFolder_t"] = pydantic.Field(
        default_factory=tuple, alias="Folder"
    )
    course_name_ref: Sequence[NameKeyReference_t] = pydantic.Field(
        default_factory=tuple, alias="CourseNameRef"
    )
    notes: str | None = pydantic.Field(default=None, alias="Notes")
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.
    name: str = pydantic.Field(alias="@Name")


class Course_t(pydantic.BaseModel):
    name: Optional["RestrictedToken_t"] = pydantic.Field(default=None, alias="Name")
    lap: Sequence["CourseLap_t"] = pydantic.Field(default_factory=tuple, alias="Lap")
    track: Sequence[Track_t] = pydantic.Field(default_factory=tuple, alias="Track")
    notes: str | None = pydantic.Field(default=None, alias="Notes")
    course_point: Sequence["CoursePoint_t"] = pydantic.Field(
        default_factory=tuple, alias="CoursePoint"
    )
    creator: Optional["AbstractSource_t"] = pydantic.Field(
        default=None, alias="Creator"
    )
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.


class CourseLap_t(pydantic.BaseModel):
    total_time_seconds: float | None = pydantic.Field(
        default=None, alias="TotalTimeSeconds"
    )
    distance_meters: float | None = pydantic.Field(default=None, alias="DistanceMeters")
    begin_position: Position_t | None = pydantic.Field(
        default=None, alias="BeginPosition"
    )
    begin_altitude_meters: float | None = pydantic.Field(
        default=None, alias="BeginAltitudeMeters"
    )
    end_position: Position_t | None = pydantic.Field(default=None, alias="EndPosition")
    end_altitude_meters: float | None = pydantic.Field(
        default=None, alias="EndAltitudeMeters"
    )
    average_heart_rate_bpm: HeartRateInBeatsPerMinute_t | None = pydantic.Field(
        default=None, alias="AverageHeartRateBpm"
    )
    maximum_heart_rate_bpm: HeartRateInBeatsPerMinute_t | None = pydantic.Field(
        default=None, alias="MaximumHeartRateBpm"
    )
    intensity: Optional["Intensity_t"] = pydantic.Field(default=None, alias="Intensity")
    cadence: Optional["CadenceValue_t"] = pydantic.Field(default=None, alias="Cadence")
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.


class CoursePoint_t(pydantic.BaseModel):
    name: Optional["CoursePointName_t"] = pydantic.Field(default=None, alias="Name")
    time: datetime.datetime | None = pydantic.Field(default=None, alias="Time")
    position: Position_t | None = pydantic.Field(default=None, alias="Position")
    altitude_meters: float | None = pydantic.Field(default=None, alias="AltitudeMeters")
    point_type: Optional["CoursePointType_t"] = pydantic.Field(
        default=None, alias="PointType"
    )
    notes: str | None = pydantic.Field(default=None, alias="Notes")
    extensions: Optional["Extensions_t"] = pydantic.Field(
        default=None, alias="Extensions"
    )  # You can extend Training Center by adding your own elements from another schema here.


class Extensions_t(pydantic.BaseModel):
    ...
    """This schema defines the Garmin Training Center file format."""


@xsds.register(
    xsds.Schema(
        name="tcxv2_2",
        namespace="https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd",
        paths_for_intermediate={
            "latitude": (
                "TrainingCenterDatabase",
                "Activities",
                "Activity",
                "Lap",
                "Track",
                "Trackpoint",
                "Position",
                "LatitudeDegrees",
            ),
            "longitude": (
                "TrainingCenterDatabase",
                "Activities",
                "Activity",
                "Lap",
                "Track",
                "Trackpoint",
                "Position",
                "LongitudeDegrees",
            ),
            "altitude": (
                "TrainingCenterDatabase",
                "Activities",
                "Activity",
                "Lap",
                "Track",
                "Trackpoint",
                "AltitudeMeters",
            ),
        },
    )
)
class Document(pydantic.BaseModel):
    __xsd_data__ = {
        "@xmlns": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
        "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        "@targetNamespace": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
        "@xmlns:tc2": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
        "@elementFormDefault": "qualified",
    }

    training_center_database: TrainingCenterDatabase_t | None = pydantic.Field(
        default=None, alias="TrainingCenterDatabase"
    )

    @staticmethod
    def from_xml(path: str) -> "Document":
        """Read a file as a document."""
        force_list = {
            ("TrainingCenterDatabase", "Activities", "MultiSportSession"),
            ("TrainingCenterDatabase", "Courses", "Course", "CoursePoint"),
            ("TrainingCenterDatabase", "Courses", "Course", "Track"),
            ("TrainingCenterDatabase", "Workouts", "Workout"),
            ("TrainingCenterDatabase", "Activities", "MultiSportSession", "NextSport"),
            ("TrainingCenterDatabase", "Workouts", "Workout", "ScheduledOn"),
            ("TrainingCenterDatabase", "Courses", "Course", "Lap"),
            ("TrainingCenterDatabase", "Activities", "Activity"),
            ("TrainingCenterDatabase", "Workouts", "Workout", "Step"),
            ("TrainingCenterDatabase", "Courses", "Course"),
            ("TrainingCenterDatabase", "Activities", "Activity", "Lap"),
        }
        string: str
        if path.startswith("http"):
            string = urllib.request.urlopen(path)
        else:
            with open(path, "r") as fp:
                string = fp.read()
        return Document(
            **xmltodict.parse(
                string,
                force_list=lambda path, key, _: (
                    tuple(p[0] for p in path) + (key,) in force_list
                ),
            )
        )

    def to_xml(
        self, path: str | None = None, namespace_keys: Sequence[str] | None = None
    ) -> str:
        """Convert this document to an XML file.

            Parameters
            ----------
                    namespace_keys : Sequence[str], optional. Defaults to all namespace keys.
        Which namespace_keys to include in the root (taken from `__xsd_data__`).
        """
        namespace_keys = (
            namespace_keys if namespace_keys is not None else tuple(self.__xsd_data__)
        )
        data = self.model_dump(exclude_none=True, by_alias=True)
        root = next(iter(data.keys()))
        data[root] = {
            **{k: v for k, v in self.__xsd_data__.items() if k in namespace_keys},
            **data[root],
        }
        output = xmltodict.unparse(data)
        if path is not None:
            with open(path, "w") as fp:
                fp.write(output)
        return output
