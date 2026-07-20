from langchain_core.tools import tool
import json
from urllib import parse, request
from pydantic import BaseModel, Field

#-------------------------------------------------------------------
# weather tool
#-------------------------------------------------------------------
# Open-Meteo WMO weather code descriptions (simplified)
WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}


class WeatherResult(BaseModel):
    """Structured result for date, time, timezone, day of week."""
    city: str = Field(description="The normalized city name"),
    lat: float = Field(description="latitude"),
    lon: float = Field(description="longitude"),
    temp: float = Field(description="temperature"),
    unit: str = Field(description="unit of measure, F or C"),
    humidity: int = Field(description="humidity"),
    description: str = Field(description="weather description based of the weather code"),


@tool("get_weather_tool", description="Used to find weather related information for the given location.")
def get_weather_tool(city: str) -> WeatherResult:
    """Fetch real weather for a city using Open-Meteo (no API key)."""
    try:
        # Geocode city name to coordinates
        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocode_params = urllib.parse.urlencode({"name": city, "count": 1})
        with urllib.request.urlopen(f"{geocode_url}?{geocode_params}", timeout=10) as r:
            geo = json.loads(r.read().decode())
        results = geo.get("results")
        if not results:
            return f"Could not find a location named '{city}'."
        lat = results[0]["latitude"]
        lon = results[0]["longitude"] 
        name = results[0].get("name", city)

        # Fetch current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = urllib.parse.urlencode({
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
        })
        with urllib.request.urlopen(f"{weather_url}?{weather_params}", timeout=10) as r:
            data = json.loads(r.read().decode())
        current = data.get("current", {})
        code = current.get("weather_code", 0)

        result = WeatherResult(
            city=name,
            lat=lat,
            lon=lon,
            temp=current.get("temperature_2m"),
            unit=data.get("current_units", {}).get("temperature_2m", "°C"),
            humidity=current.get("relative_humidity_2m"),
            description=WEATHER_CODES.get(code, "unknown conditions"),
        )

        return result.model_dump_json()
    
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        return f"Could not fetch weather for '{city}': {e}."


# Need to comment out the @tool() decorator if calling directly
if __name__ == "__main__":
   print(get_weather_tool("Parker"))
