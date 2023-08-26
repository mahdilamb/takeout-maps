import datetime
import os
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import takeout_maps
import takeout_maps.constants
from takeout_maps import takeout as takeout_queries
from takeout_maps.api import serving
from takeout_maps.routes import fitbit, takeout

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(takeout_maps.constants.PACKAGE_ROOT, "static")),
    name="static",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        f"http://localhost:{takeout_maps.constants.SHARED_WITH_FRONTEND['frontend']['port']}",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(fitbit.router)
app.include_router(takeout.router)


@app.get(
    "/connections",
    response_model=list[serving.Connection],
)
def list_connections():
    """Get a list of the available connections."""
    return [
        route.endpoint()
        for route in app.router.routes
        if route.path.endswith("/connection")
    ]


@app.get("/locations/{date}.json")
async def locations(
    date: Annotated[datetime.date, takeout.ValidRange],
) -> serving.LocationData:
    try:
        takeout.ValidRange(date)
    except ValueError as e:
        raise HTTPException(
            404,
            detail=serving.ExceptionDetail(
                errorMessage="The date is out of range.",
                errorID="date-out-of-range",
                start=str(takeout.all_range[0]),
                end=str(takeout.all_range[1]),
            ).model_dump(),
        ) from e
    return serving.LocationData(
        locations=[
            serving.Location(
                latitude=location.latitude_e7 / 1e7,
                longitude=location.longitude_e7 / 1e7,
                timestamp=location.timestamp,
                accuracy=location.accuracy,
                altitude=location.accuracy,
            )
            for location in takeout_queries.records_by_date(date).locations
        ],
        start=takeout.all_range[0].date(),
        end=takeout.all_range[1].date(),
    )


if __name__ == "__main__":
    import uvicorn

    import takeout_maps

    module = os.path.relpath(
        __file__, os.path.dirname(os.path.dirname(takeout_maps.__file__))
    ).replace(os.path.sep, ".")[:-3]
    uvicorn.run(
        f"{module}:app",
        reload=True,
        port=takeout_maps.constants.PORT,
        host=takeout_maps.constants.HOST,
    )
