import time
from threading import Lock
import requests
from fastapi import FastAPI, HTTPException

"""
    No live data is available regarding bike rental. Only available data are station information and station status.
"""
app = FastAPI()

"""
    URLs for fetching station information and status. These endpoints are provided by Lyft's GBFS feed.
"""
INFO_URL = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json"
STATUS_URL = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json"

# 3-minute cache TTL to reduce load on external API and improve response times.
CACHE_TTL_SECONDS = 60 * 3
_cache_lock = Lock()
_cache = {
    "timestamp": 0.0,
    "info": None,
    "status_map": None,
}

def _fetch_from_source():
    """
    Fetch station information and status directly from the source API.
     - Returns a tuple of (info, status_map) where:
        - info: List of station information dictionaries.
        - status_map: Dictionary mapping station_id to its status dictionary.
     - Raises an exception if the API call fails or returns invalid data.
    """
    info = requests.get(INFO_URL, timeout=(3, 10)).json()["data"]["stations"]
    status = requests.get(STATUS_URL, timeout=(3, 10)).json()["data"]["stations"]
    status_map = {s["station_id"]: s for s in status}
    return info, status_map

def fetch_station_data(force_refresh: bool = False):
    """
        Fetch and merge station data with 3-minute in-memory cache.
        - If force_refresh is True, bypass the cache and fetch fresh data from the source.
        - If the cache is valid (not expired and contains data), return cached data.
    """
    # Get the current time of the request
    now = time.monotonic()

    # Check cache validity under lock to ensure thread safety
    with _cache_lock:
        """
            Cache is valid if:
             - force_refresh is False
             - Cached info and status_map are not None (data is actually present)
            - The time since the last cache update is less than the defined TTL
        """
        cache_valid = (
            not force_refresh
            and _cache["info"] is not None
            and _cache["status_map"] is not None
            and (now - _cache["timestamp"] < CACHE_TTL_SECONDS)
        )
        # If the cache is valid, return the cached data immediately
        if cache_valid:
            return _cache["info"], _cache["status_map"]

    # Otherwise, fetch fresh data from the source API
    try:
        info, status_map = _fetch_from_source()
    except Exception as e:
        # Fallback to stale cache if available
        with _cache_lock:
            if _cache["info"] is not None and _cache["status_map"] is not None:
                return _cache["info"], _cache["status_map"]
        raise HTTPException(status_code=503, detail=f"Failed to fetch station data: {str(e)}")
    
    # Update the cache with the new data and timestamp under lock to ensure thread safety
    with _cache_lock:
        _cache["timestamp"] = time.monotonic()
        _cache["info"] = info
        _cache["status_map"] = status_map

    return info, status_map

@app.get("/stations")
def get_stations():
    """
        Get a list of all stations with their current bike and dock availability.
    """
    info, status_map = fetch_station_data()
    
    merged = []
    for s in info:
        st = status_map.get(s["station_id"], {})
        merged.append({
            "id": s["station_id"],
            "name": s["name"],
            "lat": s["lat"],
            "lon": s["lon"],
            "bikes": st.get("num_bikes_available", 0),
            "docks": st.get("num_docks_available", 0)
        })
    
    return merged

@app.get("/stations/empty")
def get_empty_stations():
    """Get all stations with no bikes available."""
    info, status_map = fetch_station_data()
    
    empty_stations = []
    for s in info:
        st = status_map.get(s["station_id"], {})
        if st.get("num_bikes_available", 0) == 0:
            empty_stations.append({
                "id": s["station_id"],
                "name": s["name"],
                "lat": s["lat"],
                "lon": s["lon"],
                "bikes": 0,
                "docks": st.get("num_docks_available", 0)
            })
    
    return empty_stations

@app.get("/stations/{station_id}")
def get_station(station_id: str):
    info, status_map = fetch_station_data()
    
    for s in info:
        if s["station_id"] == station_id:
            st = status_map.get(s["station_id"], {})
            return {
                "id": s["station_id"],
                "name": s["name"],
                "lat": s["lat"],
                "lon": s["lon"],
                "bikes": st.get("num_bikes_available", 0),
                "docks": st.get("num_docks_available", 0)
            }
    
    raise HTTPException(status_code=404, detail="Station not found")
