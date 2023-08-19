"""Script to generate the schema from XSD files."""
import os

import black
import isort.main
from xsdtopydantic import converter

import takeout_maps.xsds as xsds

OUTPUT_PATH = os.path.normpath(
    os.path.join(__file__, "..", "..", "takeout_maps", "api", "xsd")
)
schemas = xsds.Schema(
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
), xsds.Schema(
    name="gpx1_1",
    namespace="https://www.topografix.com/GPX/1/1/gpx.xsd",
    paths_for_intermediate={
        "latitude": ("gpx", "trk", "trkseg", "trkpt", "@lat"),
        "longitude": ("gpx", "trk", "trkseg", "trkpt", "@lon"),
        "elevation": ("gpx", "trk", "trkseg", "trkpt", "ele"),
    },
)


for schema in schemas:
    py_path = os.path.join(OUTPUT_PATH, f"{schema.name}.py")
    script = (
        f"import {xsds.__name__} as xsds\n"
        + converter.convert(schema.namespace, max_depth=5)
    ).splitlines()
    register = next(
        i for i, line in enumerate(script) if line.startswith("class Document")
    )
    script.insert(register, f"@xsds.register(xsds.{str(schema)})")
    with open(py_path, "w") as fp:
        fp.write("\n".join(script))

    isort.file(py_path)

black.main([OUTPUT_PATH])
