import datetime

import pytest
from faker import Faker

from core.clients.api_client import APIClient


@pytest.fixture(scope='session')
def api_client():
    client = APIClient()
    client.auth()
    return client


@pytest.fixture()
def booking_dates():
    today = datetime.date.today()
    checking_date = today + datetime.timedelta(days=10)
    checkout_date = checking_date + datetime.timedelta(days=5)

    return {
        "checkin": checking_date.strftime("%Y-%m-%d"),
        "checkout": checkout_date.strftime("%Y-%m-%d"),
    }


@pytest.fixture()
def generate_random_booking_data(booking_dates):
    faker = Faker()
    first_name = faker.first_name()
    last_name = faker.last_name()
    total_price = faker.random_number(digits=3)
    deposit_paid = faker.boolean()
    additional_needs = faker.word()

    data = {
        "firstname": first_name,
        "lastname": last_name,
        "totalprice": total_price,
        "depositpaid": deposit_paid,
        "additionalneeds": additional_needs,
        "bookingdates": booking_dates,

    }

    return data

@pytest.fixture()
def booking_dates_checkout_before_checkin():
    today = datetime.date.today()
    checking_date = today + datetime.timedelta(days=5)
    checkout_date = checking_date + datetime.timedelta(days=1)

    return {
        "checkin": checking_date.strftime("%Y-%m-%d"),
        "checkout": checkout_date.strftime("%Y-%m-%d"),
    }

@pytest.fixture()
def generate_booking_data_checkout_before_checkin(booking_dates_checkout_before_checkin):
    faker = Faker()
    first_name = faker.first_name()
    last_name = faker.last_name()
    total_price = faker.random_number(digits=3)
    deposit_paid = faker.boolean()
    additional_needs = faker.word()

    data = {
        "firstname": first_name,
        "lastname": last_name,
        "totalprice": total_price,
        "depositpaid": deposit_paid,
        "additionalneeds": additional_needs,
        "bookingdates": booking_dates_checkout_before_checkin,

    }

    return data