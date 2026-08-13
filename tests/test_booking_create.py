from http.client import responses

import allure
import jsonschema

from core.shemas.create_booking_schema import CREATE_BOOKING_RESPONSE_SCHEMA


@allure.feature("Tests Ping")
class TestBooking:

    @allure.suite("Happy path: success create booking")
    def test_success_create_booking(self, api_client, generate_random_booking_data):
        response = api_client.create_booking(generate_random_booking_data)
        response.raise_for_status()

        with allure.step('Assert status code'):
            assert response.status_code == 200, f' Expected status code 200 but got {response.status_code}'

        with allure.step('Validate response schema'):
            response_json = response.json()
            jsonschema.validate(response_json, CREATE_BOOKING_RESPONSE_SCHEMA)

        assert isinstance(
            response_json["bookingid"], int
        ), f"Booking id is not an integer, got {type(response['bookingid'])}"
        assert response_json['booking'] == generate_random_booking_data, f"Expected booking data is {generate_random_booking_data}, got {response['bookingid']}"

    @allure.feature("Negative test: check-out before check-in")
    def test_negative_checkout_before_checkin(self, api_client, generate_booking_data_checkout_before_checkin):
        response = api_client.create_booking(generate_booking_data_checkout_before_checkin)

        with allure.step('Assert status code'):
            assert response.status_code == 400


