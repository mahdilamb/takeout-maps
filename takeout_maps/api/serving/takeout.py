import datetime

import pydantic

from takeout_maps.api.takeout import semantic_location_history


class Activity(pydantic.BaseModel):
    id: int
    start: datetime.datetime
    end: datetime.datetime
    type: semantic_location_history.ActivityType
