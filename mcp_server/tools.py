import httpx

BASE="http://localhost:9001"


async def fetch(path):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE}{path}")
        r.raise_for_status()
        return r.json()


# ---------- BLR VDMS ----------
async def blr_site_status():
    return await fetch("/vdms/blr/site")

async def blr_asset_ids():
    return await fetch("/vdms/blr/assets")

async def blr_asset(asset_id:str):
    return await fetch(f"/vdms/blr/assets/{asset_id}")


# ---------- Mumbai VDMS ----------
async def mum_site_status():
    return await fetch("/vdms/mum/site")

async def mum_asset_ids():
    return await fetch("/vdms/mum/assets")

async def mum_asset(asset_id:str):
    return await fetch(f"/vdms/mum/assets/{asset_id}")


# ---------- Singapore VDMS ----------
async def sin_site_status():
    return await fetch("/vdms/sin/site")

async def sin_asset_ids():
    return await fetch("/vdms/sin/assets")

async def sin_asset(asset_id:str):
    return await fetch(f"/vdms/sin/assets/{asset_id}")

# ---------- IOC ----------
async def ioc_alerts():
    return await fetch("/ioc/alerts")

async def ioc_metrics():
    return await fetch("/ioc/metrics")

async def ioc_maintenance():
    return await fetch("/ioc/maintenance")


async def search_bangalore_assets(
    key:str,
    value:str
):
    return await fetch(
      f"/vdms/blr/assets/search?key={key}&value={value}"
    )

