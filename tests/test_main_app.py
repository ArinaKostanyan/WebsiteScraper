import sys
from fastapi.testclient import TestClient
from pathlib import Path

from app import fastapi_app


sys.path.insert(0, str(Path("scrapping_floorplan_data").resolve()))
client = TestClient(fastapi_app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_get_floorplans_by_filters():
    # Test with no filters
    response = client.get("/floorplans")
    assert response.status_code == 200

    response = client.get(
        "/floorplans?price_min=1000&price_max=3000&number_of_bedrooms=2"
    )
    assert response.status_code == 200
    assert "Filtered rows: " in response.text


def test_get_floorplans_by_property_name():
    response = client.get("/floorplans/Tempe Apartment Community")
    assert response.status_code == 200
    assert {
        "website": "https://www.example.com/tempe-apartment-community",
        "id": 1,
        "name": "Tempe Apartment Community",
    } == response.json()


def test_get_interested_by_user_id():
    response = client.get("/interested/1")
    assert response.status_code == 200
    assert "Interested floorplans found with the given user ID" in response.text
