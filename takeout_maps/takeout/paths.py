"""Paths to the takeout file."""
# TODO (Mahdi): Use the zip file rather than the extracted.
import argparse
import glob
import os

import takeout_maps.constants
from takeout_maps.takeout import utils


@utils.local_cache
def takeout_path() -> str:
    """Get the path to the google takeout."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--takeout", default=os.getenv("GOOGLE_TAKEOUT_DIRECTORY"))
    args = parser.parse_args()
    return args.takeout or os.getenv("GOOGLE_TAKEOUT_DIRECTORY")


@utils.local_cache
def records_path() -> str:
    """Get the path to the records."""
    return os.path.normpath(
        os.path.join(
            takeout_path,
            "Takeout",
            "Location History",
            "Records.json",
        )
    )


@utils.local_cache
def semantic_location_histories() -> tuple[str, ...]:
    """Get a list of all the semantic location histories."""
    return tuple(
        glob.glob(
            os.path.normpath(
                os.path.join(
                    takeout_path,
                    "Takeout",
                    "Location History",
                    "Semantic Location History",
                    "*",
                    "*.json",
                )
            )
        )
    )


def semantic_location_history(year: int, month: int):
    """Get the path to a semantic location history from the date."""
    return os.path.normpath(
        os.path.join(
            takeout_path,
            "Takeout",
            "Location History",
            "Semantic Location History",
            f"{year}",
            f"{year}_{takeout_maps.constants.MONTHS[month-1]}.json",
        )
    )
