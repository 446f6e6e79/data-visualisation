from pathlib import Path
import sys
import requests


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


BASE_URL = "http://127.0.0.1:8000"
DEFAULT_TIMEOUT = 10


def test_docs_endpoint_is_available():
    """Test that the /docs endpoint is available and returns a 200 status code."""
    response = requests.get(f"{BASE_URL}/docs", timeout=DEFAULT_TIMEOUT)

    assert response.status_code == 200

def test_get_rides_returns_mock_dataset_records():
    """Test that the /rides endpoint returns the expected mock dataset records."""
    response = requests.get(f"{BASE_URL}/rides/", timeout=DEFAULT_TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert {ride["ride_id"] for ride in payload} == {
        "85744AF35D7F2DF5",
        "9D18958E5788880B",
    }


def test_get_ride_by_id_returns_expected_mock_record():
    """Test that the /rides/by_ride_id endpoint returns the expected mock dataset record."""
    response = requests.get(
        f"{BASE_URL}/rides/by_ride_id/85744AF35D7F2DF5",
        timeout=DEFAULT_TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["ride_id"] == "85744AF35D7F2DF5"
    assert payload["rideable_type"] == "electric_bike"


def test_ride_type_statistics_uses_mock_dataset():
    """Test that the /statistics/ride-types/{rideable_type} endpoint returns statistics based on the mock dataset."""
    response = requests.get(
        f"{BASE_URL}/statistics/ride-types/classic_bike",
        timeout=DEFAULT_TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["rideable_type"] == "classic_bike"
    assert payload["stats"]["total_rides"] == 1


def test_user_type_statistics_uses_mock_dataset():
    """Test that the /statistics/user-types/{user_type} endpoint returns statistics based on the mock dataset."""
    response = requests.get(
        f"{BASE_URL}/statistics/user-types/member",
        timeout=DEFAULT_TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["user_type"] == "member"
    assert payload["stats"]["total_rides"] == 2


