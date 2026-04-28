import json
from pathlib import Path
from fastapi import FastAPI, HTTPException

app = FastAPI()

DATA_DIR = Path(__file__).parent / "data"


def load(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)


def getAssets(data):
    res = {}

    for a in data["assets"]:

        asset_type = a.get("type")
        asset_id = a.get("asset_id")

        if asset_type not in res:
            res[asset_type] = []

        res[asset_type].append(asset_id)

    return res




@app.get("/vdms/blr/site")
def blr_site():
    return load("vdms_blr.json")


@app.get("/vdms/blr/assets")
def blr_asset_ids():
    return getAssets(load("vdms_blr.json"))

# ----------------------------
# VDMS 1 (Bangalore)
# ----------------------------
@app.get("/vdms/blr/assets/search")
def search_assets(key: str, value: str):
    data = load("vdms_blr.json")

    matches = []

    value = value.lower()

    def search_nested(obj, target_key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == target_key:
                    return v
                if isinstance(v, (dict, list)):
                    found = search_nested(v, target_key)
                    if found is not None:
                        return found

        if isinstance(obj, list):
            for item in obj:
                found = search_nested(item, target_key)
                if found is not None:
                    return found

        return None

    for asset in data["assets"]:

        field = search_nested(asset, key)

        if field is None:
            continue

        if str(field).lower() == value:
            matches.append(
                asset["asset_id"]
            )

    return {
        "query": {"key": key, "value": value},
        "count": len(matches),
        "results": matches,
    }


@app.get("/vdms/blr/assets/{asset_id}")
def blr_asset(asset_id: str):
    data = load("vdms_blr.json")

    for a in data["assets"]:
        if a["asset_id"] == asset_id:
            return a

    raise HTTPException(404, "not found")


# ----------------------------
# VDMS 2 (Mumbai)
# ----------------------------


@app.get("/vdms/mum/site")
def mum_site():
    return load("vdms_mum.json")


@app.get("/vdms/mum/assets")
def mum_asset_ids():
    return getAssets(load("vdms_mum.json"))


@app.get("/vdms/mum/assets/{asset_id}")
def mum_asset(asset_id: str):
    data = load("vdms_mum.json")

    for a in data["assets"]:
        if a["asset_id"] == asset_id:
            return a

    raise HTTPException(404, "not found")


# ----------------------------
# VDMS 3 (Singapore)
# ----------------------------


@app.get("/vdms/sin/site")
def sin_site():
    return load("vdms_sin.json")


@app.get("/vdms/sin/assets")
def sin_asset_ids():
    return getAssets(load("vdms_sin.json"))


@app.get("/vdms/sin/assets/{asset_id}")
def sin_asset(asset_id: str):
    data = load("vdms_sin.json")

    for a in data["assets"]:
        if a["asset_id"] == asset_id:
            return a

    raise HTTPException(404, "not found")


# ----------------------------
# IOC logical server
# ----------------------------


@app.get("/ioc/alerts")
def alerts():
    return load("ioc.json")["alerts"]


@app.get("/ioc/metrics")
def metrics():
    return load("ioc.json")["global_metrics"]


@app.get("/ioc/maintenance")
def maintenance():
    return load("ioc.json")["maintenance_summary"]


from fastapi import HTTPException


