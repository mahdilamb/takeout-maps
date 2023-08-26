import json
import urllib.parse

from fitbit_web import auth
from pydantic2ts import generate_typescript_defs

from takeout_maps.api import serving

fitbit_redirect_url = urllib.parse.urlparse(auth.REDIRECT_URL)


host, port = fitbit_redirect_url.netloc.split(":")

SHARED = dict(
    backend=dict(host=host, port=int(port), scheme=fitbit_redirect_url.scheme),
    frontend=dict(port=5173),
)

generate_typescript_defs(
    serving.__name__, "web/src/lib/shared.ts", json2ts_cmd="npx --prefix web json2ts"
)
with open("shared.json", "w") as fp:
    json.dump(SHARED, fp)
