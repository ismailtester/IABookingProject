import pytest
import allure
import copy
import requests
from conftest import api_client
from pydantic import ValidationError
from core.models.booking import BookingResponse

@allure.feature("Test creating booking")
@allure.story("Positive: creating booking with random data and all fields")
def test_create_booking_with_custom_data(api_client, generate_random_booking_data):
    payload = generate_random_booking_data
    response_json = api_client.create_booking(payload)
    try:
        BookingResponse(**response_json)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed {e}")

    assert response_json["booking"]["firstname"] == payload["firstname"]
    assert response_json["booking"]["lastname"] == payload["lastname"]
    assert response_json["booking"]["totalprice"] == payload["totalprice"]
    assert response_json["booking"]["depositpaid"] == payload["depositpaid"]
    assert response_json["booking"]["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
    assert response_json["booking"]["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]
    assert response_json["booking"]["additionalneeds"] == payload["additionalneeds"]



@allure.feature("Test creating booking")
@allure.story("Create booking with only required fields and valid data")
def test_create_booking_with_required_fields_only	(api_client, generate_random_booking_data):
    payload = copy.deepcopy(generate_random_booking_data)
    payload.pop("additionalneeds", None) #Удаляем необязательное поле, additionalneeds
    response_json = api_client.create_booking(payload)
    try:
        BookingResponse(**response_json)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed {e}")

    assert response_json["booking"]["firstname"] == payload["firstname"]
    assert response_json["booking"]["lastname"] == payload["lastname"]
    assert response_json["booking"]["totalprice"] == payload["totalprice"]
    assert response_json["booking"]["depositpaid"] == payload["depositpaid"]
    assert response_json["booking"]["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
    assert response_json["booking"]["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]


@allure.feature("Test creating booking")
@allure.story("Create booking with empty payload")
def test_create_booking_empty_payload(api_client):
    with pytest.raises(requests.HTTPError) as exc_info:
        api_client.create_booking({})  # Пустой словарь

    status_code = exc_info.value.response.status_code
    assert status_code == 500, f"Expected 500 Bad Request, but got {status_code}"


@pytest.mark.xfail(reason="Known bug: API returns 500 instead of 400 on invalid input")
@allure.feature("Test Create Booking")
@allure.story("Create booking with only required fields and invalid data")
@pytest.mark.parametrize("field,value", [
    ("firstname", 123123),
    ("lastname", 123123),
    ("totalprice", "cheap"),
    ("depositpaid", "not paid"),
    ("bookingdates", "12.04.2025")
])
def test_create_booking_with_invalid_data(api_client, generate_random_booking_data, field, value):
    payload = copy.deepcopy(generate_random_booking_data)
    payload[field] = value
    with pytest.raises(requests.HTTPError) as exc_info:
        api_client.create_booking(payload)
    status_code = exc_info.value.response.status_code
    assert status_code == 400, f"Expected 400 Bad Request, but got {status_code}"

@allure.story("Create booking with empty payload")
@pytest.mark.xfail(reason="Known bug: API returns 500 instead of 400 on empty body")
def test_create_booking_empty_payload(api_client):
    with pytest.raises(requests.HTTPError) as exc_info:
        api_client.create_booking({})  # Пустой словарь

    status_code = exc_info.value.response.status_code
    assert status_code == 400, f"Expected 400 Bad Request, but got {status_code}"