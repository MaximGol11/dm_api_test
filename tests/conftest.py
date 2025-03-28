from collections import namedtuple
from datetime import datetime

import pytest
from faker import Faker
import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConf
from restclient.configuration import Configuration as DmApiConf
from services.serv_api_mailhog import MailHogApi
from services.serv_dm_api_account import DMApiAccount


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            #sort_keys=True
        )
    ]
)


@pytest.fixture
def account_api():
    dm_api_conf = DmApiConf(host="http://5.63.153.31:5051", disable_log=False)
    account = DMApiAccount(dm_api_conf)
    return account


@pytest.fixture
def mailhog_api():
    mailhog_conf = MailhogConf(host="http://5.63.153.31:5025", disable_log=True)
    mailhog = MailHogApi(mailhog_conf)
    return mailhog


@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog_api=mailhog_api)
    return account_helper


@pytest.fixture
def auth_account_helper(mailhog_api, prepare_user_faker):
    dm_api_conf = DmApiConf(host="http://5.63.153.31:5051")
    account_api = DMApiAccount(dm_api_conf)

    login = prepare_user_faker.login
    password = prepare_user_faker.password
    email = prepare_user_faker.email

    account_helper = AccountHelper(dm_account_api=account_api, mailhog_api=mailhog_api)
    account_helper.register_and_activate_user(login=login, password=password, email=email)
    account_helper.auth_user(login=login, password=password)

    return account_helper


@pytest.fixture
def prepare_user_faker():
    login = Faker().user_name()
    password = Faker().password()
    email = Faker().email()

    User = namedtuple("User", ["login", "password", "email"])
    user = User(login, password, email)
    return user


@pytest.fixture
def prepare_user():
    login = f"login_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}"
    password = "qweasd"
    email = f"{login}@test.com"

    User = namedtuple("User", ["login", "password", "email"])
    user = User(login, password, email)
    return user


fake = Faker()

@pytest.fixture(params=[
    {"login": fake.user_name(), "password": fake.password(), "email": fake.email(), "expected_status": 200},  # Валидные данные
    {"login": "", "password": "ValidPass123!", "email": "valid@example.com", "expected_status": 400},  # Пустой логин
    {"login": "short", "password": "ValidPass123!", "email": "valid@example.com", "expected_status": 400},  # Короткий логин
    {"login": "validUser", "password": "", "email": "valid@example.com", "expected_status": 400},  # Пустой пароль
    {"login": "validUser", "password": "short", "email": "valid@example.com", "expected_status": 400},  # Короткий пароль
    {"login": "validUser", "password": "ValidPass123!", "email": "invalid-email", "expected_status": 400} # Невалидный email
])
def user_parametrize_test_data(request):
    return request.param