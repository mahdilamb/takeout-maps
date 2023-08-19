import pydantic

from takeout_maps.api.takeout import semantic_location_history


class Histories(pydantic.BaseModel):
    months: tuple[tuple[int, int], ...]


class History(pydantic.BaseModel):
    data: semantic_location_history.SemanticLocationHistory
