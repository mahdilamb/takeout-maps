"""Constants used throughout the module."""
import json
import os
import urllib.parse
from types import MappingProxyType

from fitbit_web import auth

import takeout_maps

SQLALCHEMY_URL = "sqlite+pysqlite:///takeout.sqlite"


MONTHS = (
    "JANUARY",
    "FEBRUARY",
    "MARCH",
    "APRIL",
    "MAY",
    "JUNE",
    "JULY",
    "AUGUST",
    "SEPTEMBER",
    "OCTOBER",
    "NOVEMBER",
    "DECEMBER",
)
MONTH_TO_INT = MappingProxyType(
    {month: index for index, month in enumerate(MONTHS, start=1)}
)

PACKAGE_ROOT = os.path.normpath(os.path.join(takeout_maps.__file__, ".."))
HOST, PORT = [
    type(val)
    for val, type in zip(
        urllib.parse.urlparse(auth.REDIRECT_URL).netloc.split(":"), (str, int)
    )
]
with open(
    os.path.normpath(os.path.join(takeout_maps.__file__, "..", "..", "shared.json")),
    "r",
) as fp:
    SHARED_WITH_FRONTEND = MappingProxyType(json.load(fp))
