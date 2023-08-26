"""Utility functions for indexing."""
import datetime
import hashlib
import os
from typing import Callable, TypeVar

from takeout_maps import constants

T = TypeVar("T")


def local_cache(fn: Callable[[], T]) -> T:
    """Store the value as the function."""
    return fn()


def stat_to_dict(result: os.stat_result | str):
    """Convert a stat_result to a dictionary."""
    if isinstance(result, str):
        result = os.stat(result)
    return {k: getattr(result, k) for k in sorted(dir(result)) if k.startswith("st_")}


def table_name(path: str):
    """Get the table name for a json file."""
    from takeout_maps.takeout import paths

    return f"{os.path.basename(paths.takeout_path)}-{os.path.splitext(os.path.basename(path))[0]}-{hashlib.sha256(str(stat_to_dict(os.stat(path))).encode()).hexdigest()}"


def semantic_location_history_to_date(path: str):
    """Get a date tuple from the json file."""
    year, month = os.path.splitext(os.path.basename(path))[0].split("_")
    return int(year), constants.MONTH_TO_INT[month]


def months(
    start: datetime.datetime,
    end: datetime.datetime | datetime.timedelta,
):
    """Get the (year,month)s for a date range."""
    if isinstance(end, datetime.timedelta):
        end = start + end
    start, end = sorted((start, end))
    if start.year == end.year:
        return tuple((start.year, month) for month in range(start.month, end.month + 1))
    ranges = [range(1, 13) for _ in range(end.year - start.year + 1)]
    ranges[0] = range(start.month, 13)
    ranges[-1] = range(1, end.month + 1)
    return tuple(
        (year, month)
        for year, months in zip(range(start.year, end.year + 1), ranges)
        for month in months
    )
