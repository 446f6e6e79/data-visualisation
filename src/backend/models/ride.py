from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RideableType(str, Enum):
    """
    Enum for the type of rideable used in the CitiBike system. Possible values include:
    - classic_bike: A traditional pedal bike
    - electric_bike: A bike with an electric motor assist;
    """
    CLASSIC_BIKE = "classic_bike"
    ELECTRIC_BIKE = "electric_bike"


class MemberCasual(str, Enum):
    """
    Enum for the type of user in the CitiBike system. Possible values include:
    - member: A registered member of the CitiBike system
    - casual: A non-member user, typically a one-time or infrequent rider
    """
    MEMBER = "member"
    CASUAL = "casual"

# Mapping of WMO weather codes to human-readable descriptions
_WMO: dict[int, str] = {
    0:  "Clear sky",
    1:  "Mainly clear",
    2:  "Partly cloudy",
    3:  "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}
    
class Weather(BaseModel):
    """Model representing hourly weather conditions for NYC."""
    time: datetime  # Hourly timestamp (Eastern Time)
    temperature: float  # Temperature at 2 m (C)
    wind_speed: float  # Wind speed at 10 m (km/h)
    precipitation: float  # Total precipitation in the hour (mm)
    weather_code: int  # WMO weather interpretation code

class Ride(BaseModel):
    ride_id: str
    rideable_type: RideableType
    started_at: datetime
    ended_at: datetime
    start_station_name: str
    start_station_id: str
    end_station_name: str
    end_station_id: str
    start_lat: float
    start_lng: float
    end_lat: float
    end_lng: float
    member_casual: MemberCasual
    weather: Optional[Weather] = None # Considered weather at start