from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

nws_api = "https://api.weather.gov"
user_agent = "weather-api/1.0"

async def make_nws(url: str) -> dict[str, Any] | None:
    """Make request to NWS API with error handling"""
    headers = {
        "User-Agent": user_agent,
        "Accept": "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print("Request failed:", e)
            return None


def format_alert(feature: dict) -> str:
    """Format alert feature into readable string"""
    props = feature["properties"]

    return f"""
    Event: {props.get('event', 'Unknown')}
    Area: {props.get('areaDesc', 'Unknown')}
    Severity: {props.get('severity', 'Unknown')}
    Description: {props.get('description', 'No description available')}
    Instructions: {props.get('instruction', 'No specific instructions')}
    """


@mcp.tool()
async def get_alert(state: str) -> str:
    """
    Get weather alerts for US states.
    Args:
        state: Two-letter US state code (e.g., CA, NY)
    """
    url = f"{nws_api}/alerts/active/area/{state}"
    data = await make_nws(url)

    if not data or "features" not in data:
        return "Not fetchable or no alerts"

    if not data["features"]:
        return "No active alerts"

    alerts = [format_alert(feature) for feature in data["features"]]

    return "\n--\n".join(alerts)


@mcp.resource("greeting://{name}")
def greeting(name:str)->str:
    """ Get personalized greeting"""
    return f"Hello {name}"

@mcp.prompt()
def greet_user(name:str,style:str="friendly")->str:
    "Generate a greeting prompt"
    styles={
        "friendly":"please write a friendly greeting",
        "formal":"please write a formal greeting",
        "casual":"please write a casual greeting",
    }

    return f"{styles.get(style,styles['friendly'])} for someone named {name}"





if __name__ == "__main__":
    mcp.run()
