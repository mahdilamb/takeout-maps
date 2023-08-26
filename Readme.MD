# Takeout maps

Preliminary project looking at exploring Google Takeout data. The package:

- Indexes takeout location data so that it can be queried efficiently
- Provides a Svelte front-end (using [leaflet.js](https://leafletjs.com/)) to show location data
- Integrates with the [Fitbit](https://fitbit.com/) web api to display steps/heartrate/etc.

## Preview

Example of displaying steps/minute over location data from a trip away in Glasgow!
![Example of displaying steps/minute over location data from a trip away in Glasgow!](./assets/Screenshot%202023-08-26%20105042.png)

# Usage

Most of the common commands are in the [Makefile](./Makefile). To run, you will need to have node installed.

Install the python requirements via:

```shell
python -m pip install -e .[all]
```

Install node requirements via

```shell
npm --prefix web i
```

To serve the page ensure the following environment variables are set (either via `.env` file,globally/IDE. etc/):

```ini
FITBIT_CLIENT_ID=??
FITBIT_CLIENT_SECRET=??
FITBIT_REDIRECT_URL=??
GOOGLE_TAKEOUT_DIRECTORY=??

```

See [fitbit-web](https://github.com/mahdilamb/fitbit-web) for more on the `FITBIT_*` keys.
To run:

```shell
python -m takeout_maps & npm --prefix web run dev -- --open --port=5173
```

# Credits

The Fitbit logos belong to Google LLC and are here for ease of use...they may be removed in the future.
