from pydantic import BaseModel


class Station(BaseModel):
    """Model representing a bike station."""
    id: str
    name: str
    lat: float
    lon: float
    bikes: int
    docks: int
