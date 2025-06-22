import pytest
import allure
import copy
import requests
from conftest import api_client
from core.schemas.booking_create_response_schema import CREATED_BOOKING_SCHEMA
import jsonschema

@allure.feature("Test Create Booking")
@allure.story("Create booking with all fields and valid data")
def test_create_booking_with_all_fields	(api_client, generate_random_booking_data):
    payload = generate_random_booking_data
    response_json = api_client.create_booking(payload)

    assert response_json["booking"] == payload
    assert "bookingid" in response_json
    jsonschema.validate(response_json, CREATED_BOOKING_SCHEMA)

@allure.feature("Test Create Booking")
@allure.story("Create booking with only required fields and valid data")
def test_create_booking_with_required_fields_only	(api_client, generate_random_booking_data):
    payload = copy.deepcopy(generate_random_booking_data)
    payload.pop("additionalneeds", None)
    response_json = api_client.create_booking(payload)

    assert response_json["booking"] == payload
    assert "bookingid" in response_json
    jsonschema.validate(response_json, CREATED_BOOKING_SCHEMA)


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

@allure.feature("Test Create Booking")
@allure.story("Test server unavailability")
def test_create_booking_server_unavailable(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mocker.patch.object(api_client.session, "post", side_effect=Exception("Server unavailable"))

    with pytest.raises(Exception, match="Server unavailable"):
        api_client.create_booking(payload)



@allure.feature("Test Create Booking")
@allure.story("Test wrong HTTP method")
def test_create_booking_wrong_method(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, "post", return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status code 200, but got 405"):
        api_client.create_booking(payload)

@allure.feature("Test Create Booking")
@allure.story("Test server error")
def test_create_booking_internal_server_error(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, "post", return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status code 200, but got 500"):
        api_client.create_booking(payload)


@allure.feature("Test Create Booking")
@allure.story("Test wrong URL")
def test_create_booking_not_found(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, "post", return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status code 200, but got 404"):
        api_client.create_booking(payload)

@allure.feature("Test Create Booking")
@allure.story("Test connection with different success code")
def test_create_booking_success_different_code(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mocker.patch.object(api_client.session, "post", return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status code 200, but got 201"):
        api_client.create_booking(payload)

@allure.feature("Test Create Booking")
@allure.story("Test timeout")
def test_create_booking_timeout(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mocker.patch.object(api_client.session, "post", side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.create_booking(payload)


