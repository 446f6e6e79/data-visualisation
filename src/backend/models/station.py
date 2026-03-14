from pydantic import BaseModel


class Station(BaseModel):
    """Model representing a bike station."""
    id: str | float # The api return a UUID string, but the historical data has numeric IDs (probably due to wrong data manipulation). To avoid issues, we allow both types.
    name: str
    lat: float
    lon: float
    bikes: int
    docks: int
