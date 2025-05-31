
import allure
from conftest import api_client
from core.schemas.booking_create_response_schema import CREATED_BOOKING_SCHEMA
import jsonschema

@allure.feature("Test Create Booking")
@allure.story("Create booking with valid data")
def test_create_booking(api_client, generate_random_booking_data):
    payload = generate_random_booking_data
    response_json = api_client.create_booking(payload)

    assert response_json["booking"] == payload
    assert "bookingid" in response_json
    jsonschema.validate(response_json, CREATED_BOOKING_SCHEMA)



