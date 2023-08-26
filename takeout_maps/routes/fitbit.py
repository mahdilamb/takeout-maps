import datetime
import os
import re
import typing
import urllib.parse
from typing import Annotated, Any, final

from fastapi import APIRouter, Depends, Path, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fitbit_web import auth, client
from pydantic import AnyUrl

import takeout_maps.api.serving.fitbit as fitbit_models
import takeout_maps.constants
from takeout_maps import exceptions
from takeout_maps.api import serving

HMS = re.compile(r"(\d{2}):(\d{2}):(\d{2})")
ZONES = {v: i for i, v in enumerate(("Out of Range", "Fat Burn", "Cardio", "Peak"))}


class FitbitAuth(OAuth2AuthorizationCodeBearer):
    """Fitbit Authentication object."""

    def __init__(
        self,
    ) -> None:
        super().__init__(
            authorizationUrl=f"https://www.fitbit.com/oauth2/authorize?response_type=code&code_challenge={auth.code_challenge(auth.CODE_VERIFIER)}&code_challenge_method=S256&redirect_uri={urllib.parse.quote(auth.REDIRECT_URL)}",
            tokenUrl="https://api.fitbit.com/oauth2/token?grant_type=authorization_code",
            refreshUrl=auth.REFRESH_URL,
            scopes={k: k for k in typing.get_args(auth.Scope)},
        )
        self.__client = None
        self.__redirect_path = urllib.parse.urlparse(auth.REDIRECT_URL).path

    def __call__(self, request: Request):
        if request.url.path == self.__redirect_path:
            self.__client = client.Client(
                tokens=auth.token_from_code(
                    urllib.parse.parse_qs(request.url.query)["code"][0]
                )
            )
        if self.__client is None:
            raise exceptions.NoFitbitAuthorizationError()
        return self.__client

    @final
    @property
    def connected(self):
        return self.__client is not None


router = APIRouter(prefix="/fitbit")

fitbit_auth = FitbitAuth()
fitbit_redirect_url = urllib.parse.urlparse(auth.REDIRECT_URL)


@router.get("/connection")
def connection_info():
    return serving.Connection(
        name="Fitbit",
        path="/fitbit",
        icon="/static/Fitbit_Logo_Black_RGB.png",
        url=auth.get_authorization_url(),
        connected=fitbit_auth.connected,
        layers=[
            serving.Layer(
                label="Steps",
                path="/steps",
                color="#999",
                color_map=serving.Linear(min="#FFC20A", max="#0C7BDC"),
                color_by="value",
            ),
            serving.Layer(
                label="Heartrate",
                path="/heartrate",
                color="#999",
                color_map=(
                    serving.Linear(
                        dmin="zones.out_of_range.min",
                        dmax="zones.out_of_range.max",
                        min="#9ecae1",
                        max="#3182bd",
                    ),
                    serving.Linear(
                        dmin="zones.fat_burn.min",
                        dmax="zones.fat_burn.max",
                        min="#FFFFE0",
                        max="#FFFF00",
                    ),
                    serving.Linear(
                        dmin="zones.cardio.min",
                        dmax="zones.cardio.max",
                        min="#FFA500",
                        max="#FF8C00",
                    ),
                    serving.Linear(
                        dmin="zones.peak.min",
                        dmax="zones.peak.max",
                        min="#FF0000",
                        max="#8B0000",
                    ),
                ),
                color_by="value",
            ),
        ],
    )


@router.get("/connect")
def connect():
    return RedirectResponse(auth.get_authorization_url())


@router.get(
    str(urllib.parse.urlparse(auth.REDIRECT_URL).path[len(router.prefix) :]),
    dependencies=[Depends(fitbit_auth)],
)
def init_client(request: Request):
    if "text/html" in request.headers["accept"].split(","):
        return HTMLResponse(
            """<html><head><script type="text/javascript">window.close()</script></head></html>"""
        )
    return {"success": True}


@router.get("/steps/{date}.json")
async def steps(
    date: Annotated[str, Path(pattern=r"((\d{4}-\d{2}-\d{2})|today)")],
    fitbit_client: Annotated[client.Client, Depends(fitbit_auth)],
) -> serving.Dataset[fitbit_models.Steps, dict[str, Any]]:
    response = await fitbit_client.aget_activities_resource_by_date_intraday(
        date, detail_level="1min"
    )
    year, month, day = re.split(
        r"(\d{4})-(\d{2})-(\d{2})", response["activities-steps"][0]["dateTime"]
    )[1:-1]
    end = datetime.timedelta(
        **{
            response["activities-steps-intraday"]["datasetType"]
            + "s": response["activities-steps-intraday"]["datasetInterval"]
        }
    )

    def process_row(val: dict[str, Any]) -> fitbit_models.Steps:
        hours, mins, secs = HMS.split(val["time"])[1:-1]
        start = datetime.datetime(*(map(int, (year, month, day, hours, mins, secs))))
        return fitbit_models.Steps(start=start, end=start + end, value=val["value"])

    return serving.Dataset[fitbit_models.Steps, dict[str, Any]](
        data=[
            process_row(steps)
            for steps in response["activities-steps-intraday"]["dataset"]
        ]
    )


@router.get("/heartrate/{date}.json")
async def heartrate(
    date: Annotated[str, Path(pattern=r"((\d{4}-\d{2}-\d{2})|today)")],
    fitbit_client: Annotated[client.Client, Depends(fitbit_auth)],
) -> serving.Dataset[fitbit_models.Heartrate, fitbit_models.HeartrateMetadata]:
    response = await fitbit_client.aget_heart_by_date_intraday(
        date, detail_level="1min"
    )
    year, month, day = re.split(
        r"(\d{4})-(\d{2})-(\d{2})", response["activities-heart"][0]["dateTime"]
    )[1:-1]
    end = datetime.timedelta(
        **{
            response["activities-heart-intraday"]["datasetType"]
            + "s": response["activities-heart-intraday"]["datasetInterval"]
        }
    )

    def process_row(val: dict[str, Any]) -> fitbit_models.Heartrate:
        hours, mins, secs = HMS.split(val["time"])[1:-1]
        start = datetime.datetime(*(map(int, (year, month, day, hours, mins, secs))))
        return fitbit_models.Heartrate(start=start, end=start + end, value=val["value"])

    zones = sorted(
        response["activities-heart"][0]["value"]["heartRateZones"],
        key=lambda v: ZONES[v["name"]],
    )
    return serving.Dataset[fitbit_models.Heartrate, fitbit_models.HeartrateMetadata](
        data=[
            process_row(measurement)
            for measurement in response["activities-heart-intraday"]["dataset"]
        ],
        metadata=fitbit_models.HeartrateMetadata(
            zones=dict(
                out_of_range=fitbit_models.MinMax[int](
                    min=zones[0]["min"], max=zones[0]["max"]
                ),
                fat_burn=fitbit_models.MinMax[int](
                    min=zones[1]["min"], max=zones[1]["max"]
                ),
                cardio=fitbit_models.MinMax[int](
                    min=zones[2]["min"], max=zones[2]["max"]
                ),
                peak=fitbit_models.MinMax[int](
                    min=zones[3]["min"], max=zones[3]["max"]
                ),
            )
        ),
    )
