import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException

import takeout_maps.api.serving.takeout as takeout_models
from takeout_maps import takeout
from takeout_maps.api import serving, utils

router = APIRouter(prefix="/takeout")
all_range = takeout.records_range


ValidRange = utils.ValidatableInterval(ge=all_range[0].date(), le=all_range[1].date())


@router.get("/activities/{date}.json")
async def activities(
    date: Annotated[datetime.date, ValidRange],
):
    try:
        ValidRange(date)
    except ValueError as e:
        raise HTTPException(404) from e
    activities = [
        (object.id, object.activity_segment)
        for object in takeout.semantic_location_history_by_date(date).timeline_objects
        if object.activity_segment is not None
    ]
    return serving.Dataset[takeout_models.Activity, dict](
        data=[
            takeout_models.Activity(
                id=activity[0],
                start=activity[1].duration.start_timestamp,
                end=activity[1].duration.end_timestamp,
                type=activity[1].activity_type,
            )
            for activity in activities
        ],
        start=all_range[0],
        end=all_range[1],
    )


@router.get("/connection")
def connection_info():
    return serving.Connection(
        name="takeout",
        path="/takeout",
        icon=None,
        url=None,
        connected=None,
        layers=[
            serving.Layer(
                label="Activity",
                path="/activities",
                group_by="id",
                color="#9999",
                color_by="type",
                color_map=serving.Categorical(
                    color_map={
                        "BOATING": "#01579b",
                        "CATCHING_POKEMON": "#db4437",
                        "CYCLING": "#4db6ac",
                        "FLYING": "#3f51b5",
                        "HIKING": "#c2185b",
                        "HORSEBACK_RIDING": "#4db6ac",
                        "IN_BUS": "#01579b",
                        "IN_CABLECAR": "#01579b",
                        "IN_FERRY": "#01579b",
                        "IN_FUNICULAR": "#01579b",
                        "IN_GONDOLA_LIFT": "#01579b",
                        "IN_PASSENGER_VEHICLE": "#01579b",
                        "IN_SUBWAY": "#01579b",
                        "IN_TAXI": "#01579b",
                        "IN_TRAIN": "#01579b",
                        "IN_TRAM": "#01579b",
                        "IN_VEHICLE": "#01579b",
                        "IN_WHEELCHAIR": "#03a9f4",
                        "KAYAKING": "#4db6ac",
                        "KITESURFING": "#4db6ac",
                        "MOTORCYCLING": "#01579b",
                        "PARAGLIDING": "#4db6ac",
                        "ROWING": "#c2185b",
                        "RUNNING": "#c2185b",
                        "SAILING": "#4db6ac",
                        "SKATEBOARDING": "#4db6ac",
                        "SKATING": "#4db6ac",
                        "SKIING": "#4db6ac",
                        "SLEDDING": "#4db6ac",
                        "SNOWBOARDING": "#4db6ac",
                        "SNOWMOBILE": "#01579b",
                        "SNOWSHOEING": "#c2185b",
                        "STILL": "#A9A9A9",
                        "SURFING": "#4db6ac",
                        "SWIMMING": "#c2185b",
                        "UNKNOWN_ACTIVITY_TYPE": "#A9A9A9",
                        "WALKING": "#03a9f4",
                        "WALKING_NORDIC": "#c2185b",
                    }
                ),
            ),
        ],
    )
