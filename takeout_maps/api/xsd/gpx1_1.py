import datetime
import urllib.request
from typing import Annotated, Literal, Optional, Sequence, TypeAlias

import annotated_types
import pydantic
import xmltodict

import takeout_maps.xsds as xsds

latitudeType: TypeAlias = Annotated[
    float, annotated_types.Le(90.0), annotated_types.Ge(-90.0)
]
longitudeType: TypeAlias = Annotated[float, annotated_types.Ge(-180.0)]
degreesType: TypeAlias = Annotated[float, annotated_types.Ge(0.0)]
dgpsStationType: TypeAlias = Annotated[
    int, annotated_types.Le(1023), annotated_types.Ge(0)
]
nonNegativeInteger: TypeAlias = Annotated[int, annotated_types.Ge(0)]
gYear: TypeAlias = Annotated[
    str, pydantic.constr(pattern=r"^[-]?\d{4,}(?:Z|[+-]{1}\d{2}[:]?\d{2})?$")
]
fixType: TypeAlias = Annotated[Literal["none", "2d", "3d", "dgps", "pps"], None]


class gpxType(pydantic.BaseModel):
    """GPX documents contain a metadata header, followed by waypoints, routes, and
    tracks.

    You can add your own elementsto the extensions section of the GPX document.
    """

    metadata: Optional["metadataType"] = pydantic.Field(
        default=None
    )  # Metadata about the file.
    wpt: Sequence["wptType"] = pydantic.Field(
        default_factory=tuple
    )  # A list of waypoints.
    rte: Sequence["rteType"] = pydantic.Field(
        default_factory=tuple
    )  # A list of routes.
    trk: Sequence["trkType"] = pydantic.Field(
        default_factory=tuple
    )  # A list of tracks.
    extensions: Optional["extensionsType"] = pydantic.Field(
        default=None
    )  # You can add extend GPX by adding your own elements from another schema here.
    version: str = pydantic.Field(alias="@version")
    creator: str = pydantic.Field(alias="@creator")


class metadataType(pydantic.BaseModel):
    """Information about the GPX file, author, and copyright restrictions goes in the
    metadata section.

    Providing rich,meaningful information about your GPX files allows others to search
    for and use your GPS data.
    """

    name: str | None = pydantic.Field(default=None)  # The name of the GPX file.
    desc: str | None = pydantic.Field(
        default=None
    )  # A description of the contents of the GPX file.
    author: Optional["personType"] = pydantic.Field(
        default=None
    )  # The person or organization who created the GPX file.
    copyright: Optional["copyrightType"] = pydantic.Field(
        default=None
    )  # Copyright and license information governing use of the file.
    link: Sequence["linkType"] = pydantic.Field(
        default_factory=tuple
    )  # URLs associated with the location described in the file.
    time: datetime.datetime | None = pydantic.Field(
        default=None
    )  # The creation date of the file.
    keywords: str | None = pydantic.Field(
        default=None
    )  # Keywords associated with the file.  Search engines or databases can use this information to classify the data.
    bounds: Optional["boundsType"] = pydantic.Field(
        default=None
    )  # Minimum and maximum coordinates which describe the extent of the coordinates in the file.
    extensions: Optional["extensionsType"] = pydantic.Field(
        default=None
    )  # You can add extend GPX by adding your own elements from another schema here.


class wptType(pydantic.BaseModel):
    """Wpt represents a waypoint, point of interest, or named feature on a map."""

    ele: float | None = pydantic.Field(
        default=None
    )  # Elevation (in meters) of the point.
    time: datetime.datetime | None = pydantic.Field(
        default=None
    )  # Creation/modification timestamp for element. Date and time in are in Univeral Coordinated Time (UTC), not local time! Conforms to ISO 8601 specification for date/time representation. Fractional seconds are allowed for millisecond timing in tracklogs.
    magvar: Optional["degreesType"] = pydantic.Field(
        default=None
    )  # Magnetic variation (in degrees) at the point
    geoidheight: float | None = pydantic.Field(
        default=None
    )  # Height (in meters) of geoid (mean sea level) above WGS84 earth ellipsoid.  As defined in NMEA GGA message.
    name: str | None = pydantic.Field(
        default=None
    )  # The GPS name of the waypoint. This field will be transferred to and from the GPS. GPX does not place restrictions on the length of this field or the characters contained in it. It is up to the receiving application to validate the field before sending it to the GPS.
    cmt: str | None = pydantic.Field(
        default=None
    )  # GPS waypoint comment. Sent to GPS as comment.
    desc: str | None = pydantic.Field(
        default=None
    )  # A text description of the element. Holds additional information about the element intended for the user, not the GPS.
    src: str | None = pydantic.Field(
        default=None
    )  # Source of data. Included to give user some idea of reliability and accuracy of data.  "Garmin eTrex", "USGS quad Boston North", e.g.
    link: Sequence["linkType"] = pydantic.Field(
        default_factory=tuple
    )  # Link to additional information about the waypoint.
    sym: str | None = pydantic.Field(
        default=None
    )  # Text of GPS symbol name. For interchange with other programs, use the exact spelling of the symbol as displayed on the GPS.  If the GPS abbreviates words, spell them out.
    type: str | None = pydantic.Field(
        default=None
    )  # Type (classification) of the waypoint.
    fix: Optional["fixType"] = pydantic.Field(default=None)  # Type of GPX fix.
    sat: nonNegativeInteger | None = pydantic.Field(
        default=None
    )  # Number of satellites used to calculate the GPX fix.
    hdop: float | None = pydantic.Field(
        default=None
    )  # Horizontal dilution of precision.
    vdop: float | None = pydantic.Field(default=None)  # Vertical dilution of precision.
    pdop: float | None = pydantic.Field(default=None)  # Position dilution of precision.
    ageofdgpsdata: float | None = pydantic.Field(
        default=None
    )  # Number of seconds since last DGPS update.
    dgpsid: Optional["dgpsStationType"] = pydantic.Field(
        default=None
    )  # ID of DGPS station used in differential correction.
    extensions: Optional["extensionsType"] = pydantic.Field(
        default=None
    )  # You can add extend GPX by adding your own elements from another schema here.
    lat: latitudeType = pydantic.Field(alias="@lat")
    lon: longitudeType = pydantic.Field(alias="@lon")


class rteType(pydantic.BaseModel):
    """rte represents route - an ordered list of waypoints representing a series of turn points leading to a destination."""

    name: str | None = pydantic.Field(default=None)  # GPS name of route.
    cmt: str | None = pydantic.Field(default=None)  # GPS comment for route.
    desc: str | None = pydantic.Field(
        default=None
    )  # Text description of route for user.  Not sent to GPS.
    src: str | None = pydantic.Field(
        default=None
    )  # Source of data. Included to give user some idea of reliability and accuracy of data.
    link: Sequence["linkType"] = pydantic.Field(
        default_factory=tuple
    )  # Links to external information about the route.
    number: nonNegativeInteger | None = pydantic.Field(
        default=None
    )  # GPS route number.
    type: str | None = pydantic.Field(default=None)  # Type (classification) of route.
    extensions: Optional["extensionsType"] = pydantic.Field(
        default=None
    )  # You can add extend GPX by adding your own elements from another schema here.
    rtept: Sequence[wptType] = pydantic.Field(
        default_factory=tuple
    )  # A list of route points.


class trkType(pydantic.BaseModel):
    """trk represents a track - an ordered list of points describing a path."""

    name: str | None = pydantic.Field(default=None)  # GPS name of track.
    cmt: str | None = pydantic.Field(default=None)  # GPS comment for track.
    desc: str | None = pydantic.Field(default=None)  # User description of track.
    src: str | None = pydantic.Field(
        default=None
    )  # Source of data. Included to give user some idea of reliability and accuracy of data.
    link: Sequence["linkType"] = pydantic.Field(
        default_factory=tuple
    )  # Links to external information about track.
    number: nonNegativeInteger | None = pydantic.Field(
        default=None
    )  # GPS track number.
    type: str | None = pydantic.Field(default=None)  # Type (classification) of track.
    extensions: Optional["extensionsType"] = pydantic.Field(
        default=None
    )  # You can add extend GPX by adding your own elements from another schema here.
    trkseg: Sequence["trksegType"] = pydantic.Field(
        default_factory=tuple
    )  # A Track Segment holds a list of Track Points which are logically connected in order. To represent a single GPS track where GPS reception was lost, or the GPS receiver was turned off, start a new Track Segment for each continuous span of track data.


class extensionsType(pydantic.BaseModel):
    """You can add extend GPX by adding your own elements from another schema here."""


class trksegType(pydantic.BaseModel):
    """A Track Segment holds a list of Track Points which are logically connected in
    order.

    To represent a single GPS track where GPS reception was lost, or the GPS receiver
    was turned off, start a new Track Segment for each continuous span of track data.
    """

    trkpt: Sequence[wptType] = pydantic.Field(
        default_factory=tuple
    )  # A Track Point holds the coordinates, elevation, timestamp, and metadata for a single point in a track.
    extensions: extensionsType | None = pydantic.Field(
        default=None
    )  # You can add extend GPX by adding your own elements from another schema here.


class copyrightType(pydantic.BaseModel):
    """Information about the copyright holder and any license governing use of this
    file.

    By linking to an appropriate license,you may place your data into the public domain
    or grant additional usage rights.
    """

    year: gYear | None = pydantic.Field(default=None)  # Year of copyright.
    license: pydantic.AnyUrl | None = pydantic.Field(
        default=None
    )  # Link to external file containing license text.
    author: str = pydantic.Field(alias="@author")


class linkType(pydantic.BaseModel):
    """A link to an external resource (Web page, digital photo, video clip, etc) with
    additional information."""

    text: str | None = pydantic.Field(default=None)  # Text of hyperlink.
    type: str | None = pydantic.Field(default=None)  # Mime type of content (image/jpeg)
    href: pydantic.AnyUrl = pydantic.Field(alias="@href")


class emailType(pydantic.BaseModel):
    """An email address.

    Broken into two parts (id and domain) to help prevent email harvesting.
    """

    id: str = pydantic.Field(alias="@id")
    domain: str = pydantic.Field(alias="@domain")


class personType(pydantic.BaseModel):
    """A person or organization."""

    name: str | None = pydantic.Field(default=None)  # Name of person or organization.
    email: emailType | None = pydantic.Field(default=None)  # Email address.
    link: linkType | None = pydantic.Field(
        default=None
    )  # Link to Web site or other external information about person.


class ptType(pydantic.BaseModel):
    """A geographic point with optional elevation and time.

    Available for use by other schemas.
    """

    ele: float | None = pydantic.Field(
        default=None
    )  # The elevation (in meters) of the point.
    time: datetime.datetime | None = pydantic.Field(
        default=None
    )  # The time that the point was recorded.
    lat: latitudeType = pydantic.Field(alias="@lat")
    lon: longitudeType = pydantic.Field(alias="@lon")


class ptsegType(pydantic.BaseModel):
    """An ordered sequence of points.

    (for polygons or polylines, e.g.)
    """

    pt: Sequence[ptType] = pydantic.Field(
        default_factory=tuple
    )  # Ordered list of geographic points.


class boundsType(pydantic.BaseModel):
    """Two lat/lon pairs defining the extent of an element."""

    minlat: latitudeType = pydantic.Field(alias="@minlat")
    minlon: longitudeType = pydantic.Field(alias="@minlon")
    maxlat: latitudeType = pydantic.Field(alias="@maxlat")
    maxlon: longitudeType = pydantic.Field(alias="@maxlon")
    """GPX schema version 1.1 - For more information on GPX and this schema, visit http://www.topografix.com/gpx.aspGPX uses the following conventions: all coordinates are relative to the WGS84 datum.  All measurements are in metric units."""


@xsds.register(
    xsds.Schema(
        name="gpx1_1",
        namespace="https://www.topografix.com/GPX/1/1/gpx.xsd",
        paths_for_intermediate={
            "latitude": ("gpx", "trk", "trkseg", "trkpt", "@lat"),
            "longitude": ("gpx", "trk", "trkseg", "trkpt", "@lon"),
            "elevation": ("gpx", "trk", "trkseg", "trkpt", "ele"),
        },
    )
)
class Document(pydantic.BaseModel):
    __xsd_data__ = {
        "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        "@xmlns": "http://www.topografix.com/GPX/1/1",
        "@targetNamespace": "http://www.topografix.com/GPX/1/1",
        "@elementFormDefault": "qualified",
    }

    gpx: gpxType | None = pydantic.Field(
        default=None
    )  # GPX is the root element in the XML file.

    @staticmethod
    def from_xml(path: str) -> "Document":
        """Read a file as a document."""
        force_list = {
            ("gpx", "rte", "rtept"),
            ("gpx", "trk", "trkseg"),
            ("gpx", "wpt"),
            ("gpx", "metadata", "link"),
            ("gpx", "rte", "link"),
            ("gpx", "rte", "rtept", "link"),
            ("gpx", "trk"),
            ("gpx", "trk", "trkseg", "trkpt"),
            ("gpx", "rte"),
            ("gpx", "wpt", "link"),
            ("gpx", "trk", "link"),
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
