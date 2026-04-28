from fastmcp import FastMCP
from tools import *

mcp = FastMCP("facility-router")


# MCP now chooses logical system
@mcp.tool()
async def get_bangalore_site_status():
    """
    Fetch all asset data of Bangalore VDMS
    Note: Only use if it is required, this tool costs more
    """
    return await blr_site_status()


@mcp.tool()
async def get_bangalore_asset(asset_id: str):
    """Query Bangalore asset using asset ID"""
    return await blr_asset(asset_id)


@mcp.tool()
async def get_bangalore_assets():
    """Get all asset IDs of Bangalore VDMS"""
    return await blr_asset_ids()


@mcp.tool()
async def get_mumbai_site_status():
    """Fetch all asset data of Mumbai VDMS
    Note: Only use if it is required, this tool costs more"""
    return await mum_site_status()


@mcp.tool()
async def get_mumbai_assets():
    """Get all asset IDs of Mumbai VDMS"""
    return await mum_asset_ids()


@mcp.tool()
async def get_mumbai_asset(asset_id: str):
    """Query Mumbai asset using asset ID"""
    return await mum_asset(asset_id)


@mcp.tool()
async def get_singapore_site_status():
    """Fetch all asset data of Singapore VDMS
    Note: Only use if it is required, this tool costs more"""
    return await sin_site_status()


@mcp.tool()
async def get_singapore_assets():
    """Get all asset IDs of Singapore VDMS"""
    return await sin_asset_ids()


@mcp.tool()
async def get_singapore_asset(asset_id: str):
    """Query Singapore asset using asset ID"""
    return await sin_asset(asset_id)


@mcp.tool()
async def get_global_alerts():
    """Query IOC alerts"""
    return await ioc_alerts()


@mcp.tool()
async def get_energy_dashboard():
    """Query IOC metrics"""
    return await ioc_metrics()

@mcp.tool()
async def get_global_maintanance_details():
    """Query IOC maintanance"""
    return await ioc_maintenance()

@mcp.tool()
async def search_bangalore_assets_by_asset_type(asset_type: str):
    """
    Find asset IDs by asset type.
    Examples:
    AC
    WiFi
    Occupancy

    Returns:
    List of matching asset IDs.
    """
    return await search_bangalore_assets("type", asset_type)


@mcp.tool()
async def search_bangalore_assets_by_vendors(vendor: str):
    """
    Find assets belonging to a vendor.
    Example:
    Daikin
    Cisco

    Returns:
    List of matching asset IDs.
    """
    return await search_bangalore_assets("vendor", vendor)


@mcp.tool()
async def search_assets_by_model(model: str):
    """
    Search Bangalore assets by equipment model
    and return matching asset IDs only.

    Use when user asks about a specific model.

    Examples:
    - Find assets with model VRV-X12
    - Which assets use model Catalyst 9300

    Valid values:
    VRV-X12
    Catalyst 9300

    Returns:
    List of matching asset IDs.
    """
    return await search_bangalore_assets(key="model", value=model)


@mcp.tool()
async def search_assets_by_mac_address(mac_address: str):
    """
    Search Bangalore assets by MAC address
    and return matching asset IDs only.

    Use when user knows device/network MAC address.

    Examples:
    - Find asset with MAC 00:1A:C2:7B:AA:10
    - Which asset has MAC 00:1B:AA:FF:90:33

    Input must be a MAC address.

    Returns:
    Matching asset IDs.
    """
    return await search_bangalore_assets(key="mac_address", value=mac_address)


@mcp.tool()
async def search_assets_by_zone(zone: str):
    """
    Search Bangalore assets by physical zone
    and return asset IDs in that zone.

    Use when user asks about assets in an area.

    Examples:
    - Assets in Floor-3-East
    - Show devices in Server Room
    - Find assets in Ground Floor

    Example zones:
    Floor-3-East
    Server Room
    Ground Floor

    Returns:
    Matching asset IDs.
    """
    return await search_bangalore_assets(key="zone", value=zone)


@mcp.tool()
async def search_assets_by_status(status: str):
    """
    Search Bangalore assets by health status
    and return matching asset IDs.

    Use for faults, warnings, healthy assets.

    Valid statuses:
    healthy
    warning
    fault

    Examples:
    - Show warning assets
    - Find fault assets
    - Which assets are healthy

    Returns:
    Matching asset IDs only.

    For questions like
    'which assets need attention'
    use status='warning' or status='fault'
    """
    return await search_bangalore_assets(key="status", value=status)


if __name__ == "__main__":
    mcp.run()
