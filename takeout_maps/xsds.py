import glob
import os
import typing
from typing import Literal, NamedTuple, TypeVar

import pydantic

import takeout_maps
from takeout_maps.api import xsd

T = TypeVar("T", bound=type[pydantic.BaseModel])


class Schema(NamedTuple):
    name: str
    namespace: str
    paths_for_intermediate: dict[
        Literal["latitude", "longitude", "altitude", "elevation"], tuple[str | int, ...]
    ]


@typing.no_type_check
def register(schema: Schema):
    def wrapper(cls: T):
        setattr(register, "__registry__", getattr(register, "__registry__", {}))
        register.__registry__[schema.name] = cls
        return cls

    return wrapper


def from_registry(name_or_schema: str | Schema) -> T:
    if isinstance(name_or_schema, Schema):
        name_or_schema = name_or_schema.name
    return getattr(register, "__registry__", {})[name_or_schema]


for file in glob.glob(os.path.normpath(os.path.join(xsd.__file__, "..", "*.py"))):
    __import__(
        os.path.relpath(
            file, os.path.normpath(os.path.join(takeout_maps.__file__, "..", ".."))
        ).replace(os.path.sep, ".")[:-3]
    )
