import argparse
import os
import urllib.parse
from typing import Annotated

import pydantic
from fastapi import Depends, FastAPI, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fitbit_web import auth, client
from pydantic_stream import resolve

from takeout_maps import exceptions, security
from takeout_maps.api import serving
from takeout_maps.api.takeout import takeout

parser = argparse.ArgumentParser()
parser.add_argument("--takeout")
args = parser.parse_args()
takeout_data = takeout.Takeout(args.takeout)

fitbit_redirect_url = urllib.parse.urlparse(auth.REDIRECT_URL)
host, port = fitbit_redirect_url.netloc.split(":")


app = FastAPI()


fitbit_auth = security.FitbitAuth()


@app.get("/history.json", response_model=serving.Histories)
def months():
    return {"months": takeout_data.semantic_location_histories}


@app.get("/history/{year}/{month}.json", response_model=serving.History)
def month(
    year: Annotated[int, pydantic.constr(pattern=r"\d{4}")],
    month: Annotated[int, pydantic.constr(pattern=r"\d{2}")],
):
    with takeout_data.semantic_location_history((year, month)) as history:
        return {"data": resolve(history)}


@app.get(str(fitbit_redirect_url.path), dependencies=[Depends(fitbit_auth)])
def init_client():
    return RedirectResponse("/")


@app.exception_handler(exceptions.NoFitbitAuthorizationError)
async def requires_fitbit(*_):
    return HTMLResponse(
        """<html>
    <body>
        <a href=\""""
        + auth.get_authorization_url()
        + """\"">Connect fitbit</a>

    </body>
</html>
"""
    )


@app.get("/")
def today():
    return RedirectResponse("/today")


@app.get("/{date}")
async def steps(
    date: Annotated[str, Path(pattern=r"((\d{4}-\d{2}-\d{2})|today)")],
    fitbit_client: Annotated[client.Client, Depends(fitbit_auth)],
):
    async with fitbit_client.async_client() as web_client:
        data = await web_client.aget_activities_resource_by_date_intraday(
            date, detail_level="1min"
        )
        return HTMLResponse(
            """<head>
	<script src='https://cdn.plot.ly/plotly-2.25.2.min.js'></script>
</head>

<body>
	<div id='myDiv'><!-- Plotly chart will be drawn inside this DIV --></div>
    <script type="text/javascript">
    var trace1 = {
  x: """
            + str(
                [
                    value["time"]
                    for value in data["activities-steps-intraday"]["dataset"]
                ]
            )
            + """,
  y: """
            + str(
                [
                    value["value"]
                    for value in data["activities-steps-intraday"]["dataset"]
                ]
            )
            + """,
  type: 'scatter'
};

Plotly.newPlot('myDiv', [trace1]);

    </script>
</body>"""
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
        port=int(port),
        host=host,
    )
