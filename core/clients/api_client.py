import requests
import os
import allure
import jsonschema

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

from core.settings.enviroments import Enviroments
from core.settings.config import Users, Timeouts
from core.clients.endpoints import Endpoints


load_dotenv()


class APIClient:
    def __init__(self):
        enviroment_str = os.getenv('ENVIRONMENT')
        try:
            enviroment = Enviroments[enviroment_str]
        except KeyError:
            raise ValueError(f'Unsupported enviroment value:  {enviroment_str} ')

        self.base_url = self.get_base_url(enviroment)
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json'
        }

    def get_base_url(self, enviroment: Enviroments):
        if enviroment == Enviroments.TEST:
            return os.getenv('TEST_BASE_URL')
        elif enviroment == Enviroments.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f'Unsupported enviroment value: {enviroment}')

    def ping(self):
        with allure.step('Ping api client'):
            url = f'{self.base_url}{Endpoints.PING_ENDPOINT}'
            response = self.session.get(url)
            response.raise_for_status()

        with allure.step('Assert status code'):
            assert response.status_code == 201, f' Expected status code 201 but got {response.status_code}'
        return response.status_code

    def auth(self):
        with allure.step('Authenticate api client'):
            url = f'{self.base_url}{Endpoints.AUTH_ENDPOINT}'
            payload = {
                "username": Users.USERNAME,
                "password": Users.PASSWORD
            }
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()

        with allure.step('Assert status code'):
            assert response.status_code == 200, f' Expected status code 200 but got {response.status_code}'
        token = response.json()['token']

        with allure.step('Updating headers with authorization'):
            self.session.headers.update({'Authorization': f'Bearer {token}'})

    def get_booking_by_id(self, booking_id):
        with allure.step('Get booking by id'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}'
            response = self.session.get(url, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()

        with allure.step('Assert status code'):
            assert response.status_code == 200, f' Expected status code 200 but got {response.status_code}'

        with allure.step('Validate get schema'):
            response_json = response.json()
            jsonschema.validate(response_json)
        return response_json

    def get_booking_ids(self, params=None):
        with allure.step('Send GET request to receive booking IDs'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}'
            response = self.session.get(url, params=params, timeout=Timeouts.TIMEOUT)

        with allure.step('Assert status code is 200'):
            assert response.status_code == 200, f'Expected status code 200 but got {response.status_code}'

        with allure.step('Extract IDs from response'):
            booking_data = response.json()
            return [item['bookingid'] for item in booking_data]

    def create_booking(self, booking_json):
        with allure.step('Create booking'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}'
            response = self.session.post(url, json=booking_json, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()

        with allure.step('Assert status code'):
            assert response.status_code == 200, f' Expected status code 200 but got {response.status_code}'

        with allure.step('Validate get schema'):
            response_json = response.json()
            jsonschema.validate(response_json)

        return response_json

    def update_booking_by_id(self, booking_id, booking_json):
        with allure.step('Update booking by id'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}'
            response = self.session.put(url, json=booking_json, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()

        with allure.step('Assert status code'):
            assert response.status_code == 200, f' Expected status code 200 but got {response.status_code}'

        with allure.step('Validate get schema'):
            response_json = response.json()
            jsonschema.validate(response_json)

        return response_json

    def partial_update_booking_by_id(self, booking_id, booking_json):
        with allure.step('Update booking by id'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}'
            response = self.session.put(url, json=booking_json, timeout=Timeouts.TIMEOUT)

        with allure.step('Assert status code is 200'):
            assert response.status_code == 200, f' Expected status code 200 but got {response.status_code}'

        with allure.step('Validate get schema'):
            response_json = response.json()
            jsonschema.validate(response_json)

        return response_json

    def delete_booking_by_id(self, booking_id):
        with allure.step('Delete booking by id'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}'
            response = self.session.delete(url, auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD), timeout=Timeouts.TIMEOUT)
            response.raise_for_status()

        with allure.step('Assert status code'):
            assert response.status_code == 201, f' Expected status code 201 but got {response.status_code}'

        return response.status_code == 201



