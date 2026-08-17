import allure
import jsonschema
import pytest
from jsonschema import ValidationError
from requests.exceptions import HTTPError

from core.models.booking import BookingRenounce
from core.shemas.create_booking_schema import CREATE_BOOKING_RESPONSE_SCHEMA


@allure.feature("Tests create booking")
class TestBooking:

    @allure.suite("Happy path: success create booking")
    def test_success_create_booking(self, api_client, generate_random_booking_data):
        response = api_client.create_booking(generate_random_booking_data)

        with allure.step('Assert status code'):
            assert response.status_code == 200, f' Expected status code 200 but got {response.status_code}'

        with allure.step('Validate response schema'):
            response_json = response.json()
            jsonschema.validate(response_json, CREATE_BOOKING_RESPONSE_SCHEMA)

        assert isinstance(
            response_json["bookingid"], int
        ), f"Booking id is not an integer, got {type(response['bookingid'])}"
        assert response_json[
                   'booking'] == generate_random_booking_data, f"Expected booking data is {generate_random_booking_data}, got {response['bookingid']}"

    @allure.suite("Negative test: Send without required fields")
    @pytest.mark.parametrize(
        "field",
        [
            "firstname",
            "lastname",
            "totalprice",
            "depositpaid",
            "bookingdates",
        ]
    )
    def test_create_booking_without_required_field(
            self,
            api_client,
            generate_random_booking_data,
            field
    ):
        with allure.step('Data preparation'):
            booking_data = generate_random_booking_data.copy()
            booking_data.pop(field)

        with allure.step(f'Send field without {field}'):
            with pytest.raises(HTTPError) as exc_info:
                api_client.create_booking(booking_data)

            response = exc_info.value.response

        with allure.step('Assert status code is 500'):
            assert response.status_code == 500, f'Expected status code 500, but got {response.status_code}'

    @allure.suite("Negative test: Send with empty boby")
    def test_create_booking_with_empty_body(
            self,
            api_client,
    ):
        with allure.step('Data preparation'):
            booking_data = {}

        with allure.step('Send empty boby'):
            with pytest.raises(HTTPError) as exc_info:
                api_client.create_booking(booking_data)

            response = exc_info.value.response

        with allure.step('Assert status code is 500'):
            assert response.status_code == 500, f'Expected status code 500, but got {response.status_code}'

    @allure.suite("Negative test: Send invalid types and invalid data")
    @pytest.mark.parametrize(
        "firstname",
        [
            25,
            None,
            True,
        ],
        ids=["number", "None", "Boolean"]
    )
    def test_create_booking_with_negative_type_firstname(
            self,
            api_client,
            generate_random_booking_data,
            firstname
    ):
        with allure.step('Data preparation'):
            booking_data = generate_random_booking_data.copy()
            booking_data["firstname"] = firstname

        with allure.step(f'Send firstname with type data {type(firstname)}'):
            with pytest.raises(HTTPError) as exc_info:
                api_client.create_booking(booking_data)

            response = exc_info.value.response

        with allure.step('Assert status code is 500'):
            assert response.status_code == 500, f'Expected status code 500, but got {response.status_code}'

    @allure.suite("Positive test: Send valid types in firstname")
    @pytest.mark.parametrize(
        "firstname",
        [
            "Васёк",
            "",
        ],
        ids=["valid_name", "empty_string"]
    )
    def test_create_booking_with_positive_type_firstname(
            self,
            api_client,
            generate_random_booking_data,
            firstname
    ):
        with allure.step('Data preparation'):
            booking_data = generate_random_booking_data.copy()
            booking_data["firstname"] = firstname

        with allure.step(f'Send firstname with type data "{firstname}"'):
            response = api_client.create_booking(booking_data)

        with allure.step('Assert status code is 500'):
            assert response.status_code == 200, f'Expected status code 200, but got {response.status_code}'

        with allure.step('Validate response schema'):
            response_json = response.json()
            jsonschema.validate(response_json, CREATE_BOOKING_RESPONSE_SCHEMA)

        with allure.step('Name match check'):
            response_json["firstname"] = booking_data["firstname"]

    @allure.suite("Positive test: create booking with random date")
    def test_create_booking_with_random_data(self, api_client, generate_random_booking_data):

        with allure.step('Data preparation'):
            booking_data = generate_random_booking_data.copy()

        with allure.step('Send request'):
            response = api_client.create_booking(booking_data)
            response_json = response.json()

        with allure.step('Validate response schema'):
            try:
                BookingRenounce(**response_json)
            except ValidationError as e:
                raise ValidationError(f'Response validation error: {e}')

        with allure.step('Comparison of sent and received data'):
            assert response_json[
                       'booking'] == generate_random_booking_data, f"Expected booking data is {generate_random_booking_data}, got {response['bookingid']}"

    @allure.suite("Positive test: create booking without additionalneeds")
    def test_create_booking_without_additionalneeds(self, api_client, generate_random_booking_data):
        with allure.step('Data preparation'):
            booking_data = generate_random_booking_data.copy()
            booking_data.pop("additionalneeds")

        with allure.step('Send request'):
            response = api_client.create_booking(booking_data)
            response_json = response.json()

        with allure.step('Validate response schema'):
            try:
                BookingRenounce(**response_json)
            except ValidationError as e:
                raise ValidationError(f'Response validation error: {e}')

    @allure.suite("Positive test: create booking with correct depositpaid")
    @pytest.mark.parametrize(
        "depositpaid",
        [True, False],
    )
    def test_create_booking_with_correct_depositpaid_data(self, api_client, generate_random_booking_data, depositpaid):
        with allure.step('Data preparation'):
            booking_data = generate_random_booking_data.copy()
            booking_data["depositpaid"] = depositpaid

        with allure.step('Send request'):
            response = api_client.create_booking(booking_data)
            response_json = response.json()

        with allure.step('Check depositpaid'):
            assert response_json[
                       'booking']["depositpaid"] == booking_data["depositpaid"]
    
    @allure.suite("Positive test: create booking with correct depositpaid")
    def test_create_booking_with_invalid_depositpaid_data(self, api_client, generate_random_booking_data):
        with allure.step('Data preparation'):
            booking_data = generate_random_booking_data.copy()
            booking_data["depositpaid"] = None

        with allure.step('Send request'):
            with pytest.raises(HTTPError) as exc_info:
                api_client.create_booking(booking_data)

            response = exc_info.value.response

        with allure.step('Assert status code is 500'):
            assert response.status_code == 500, f'Expected status code 500, but got {response.status_code}'
            assert response.text == 'Internal Server Error'
