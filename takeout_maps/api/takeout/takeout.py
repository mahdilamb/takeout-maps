import contextlib
import glob
import os
from functools import cached_property
from types import MappingProxyType
from typing import TypeAlias

from pydantic_stream import stream_model

from takeout_maps.api.takeout import records, semantic_location_history, settings

YYYY_MM: TypeAlias = tuple[int, int]
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


class Takeout:
    def __init__(self, path: str) -> None:
        self.__path = path

    @contextlib.contextmanager
    def records(self):
        try:
            with open(
                os.path.normpath(
                    os.path.join(
                        self.__path, "Takeout", "Location History", "Records.json"
                    )
                ),
                "r",
            ) as fp:
                yield stream_model(records.Records, fp)
        finally:
            ...

    @contextlib.contextmanager
    def settings(self):
        try:
            with open(
                os.path.normpath(
                    os.path.join(
                        self.__path, "Takeout", "Location History", "Settings.json"
                    )
                ),
                "r",
            ) as fp:
                yield stream_model(settings.Settings, fp)
        finally:
            ...

    @cached_property
    def semantic_location_histories(self) -> tuple[YYYY_MM, ...]:
        return tuple(
            sorted(
                tuple(
                    (int(file[:4]), MONTH_TO_INT[file[5:-5].upper()])
                    for file in map(
                        os.path.basename,
                        glob.glob(
                            os.path.join(
                                self.__path,
                                "Takeout",
                                "Location History",
                                "Semantic Location History",
                                "**",
                                "*",
                            )
                        ),
                    )
                )
            )
        )

    @contextlib.contextmanager
    def semantic_location_history(self, date: YYYY_MM):
        if date not in self.semantic_location_histories:
            raise ValueError(f"No history for the date {date}")
        try:
            with open(
                os.path.normpath(
                    os.path.join(
                        self.__path,
                        "Takeout",
                        "Location History",
                        "Semantic Location History",
                        str(date[0]),
                        f"{date[0]}_{MONTHS[date[1]-1]}.json",
                    )
                ),
                "r",
            ) as fp:
                yield stream_model(
                    semantic_location_history.SemanticLocationHistory, fp
                )
        finally:
            ...
