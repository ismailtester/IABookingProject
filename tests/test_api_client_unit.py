import pytest
import allure
import requests


@allure.feature("API Client")
@allure.story("create_booking")
@allure.title("Should raise Exception if server is unavailable")
@pytest.mark.unit
def test_create_booking_server_unavailable(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mocker.patch.object(api_client.session, "post", side_effect=Exception("Server unavailable"))

    with pytest.raises(Exception, match="Server unavailable"):
        api_client.create_booking(payload)


@allure.feature("API Client")
@allure.story("create_booking")
@allure.title("Should raise AssertionError if HTTP method not allowed (405)")
@pytest.mark.unit
def test_create_booking_wrong_method(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, "post", return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status code 200, but got 405"):
        api_client.create_booking(payload)


@allure.feature("API Client")
@allure.story("create_booking")
@allure.title("Should raise AssertionError on internal server error (500)")
@pytest.mark.unit
def test_create_booking_internal_server_error(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, "post", return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status code 200, but got 500"):
        api_client.create_booking(payload)


@allure.feature("API Client")
@allure.story("create_booking")
@allure.title("Should raise AssertionError on 404 Not Found")
@pytest.mark.unit
def test_create_booking_not_found(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, "post", return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status code 200, but got 404"):
        api_client.create_booking(payload)


@allure.feature("API Client")
@allure.story("create_booking")
@allure.title("Should raise AssertionError if success code is not 200 (e.g. 201)")
@pytest.mark.unit
def test_create_booking_success_different_code(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mocker.patch.object(api_client.session, "post", return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status code 200, but got 201"):
        api_client.create_booking(payload)


@allure.feature("API Client")
@allure.story("create_booking")
@allure.title("Should raise Timeout if request times out")
@pytest.mark.unit
def test_create_booking_timeout(api_client, mocker, generate_random_booking_data):
    payload = generate_random_booking_data
    mocker.patch.object(api_client.session, "post", side_effect=requests.Timeout)

    with pytest.raises(requests.Timeout):
        api_client.create_booking(payload)