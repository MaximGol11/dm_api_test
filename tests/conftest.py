import os
from collections import namedtuple
from datetime import datetime
from pathlib import Path

import allure
import pytest
from faker import Faker
import structlog
from requests import options
from swagger_coverage_py.reporter import CoverageReporter
from vyper import v

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

options =(
    'service.dm_api_acount',
    'service.mailhod_api',
    'telegram.bot_token',
    'telegram.chat_id'
)

@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host="http://5.63.153.31:5051")
    reporter.setup("/swagger/Account/swagger.json")

    yield
    reporter.generate_report()
    reporter.cleanup_input_files()


@pytest.fixture(scope="session", autouse=True)
def set_config(request):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()

    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))

    os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get('telegram.chat_id')
    os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get('telegram.bot_token')
    request.config.stash['telegram-notifier-addfields']['enviroment'] = config_name
    request.config.stash['telegram-notifier-addfields']['report'] = "https://maximgol11.github.io/dm_api_test/"


def pytest_addoption(parser):
    parser.addoption("--env", default="stg", action="store", help="run stg")

    for option in options:
        parser.addoption(f"--{option}", action="store", default=None, )


@pytest.fixture
def account_api():
    dm_api_conf = DmApiConf(host=v.get("service.dm_api_account"), disable_log=False)
    account = DMApiAccount(dm_api_conf)
    return account


@pytest.fixture
def mailhog_api():
    mailhog_conf = MailhogConf(host=v.get("service.mailhog_api"), disable_log=True)
    mailhog = MailHogApi(mailhog_conf)
    return mailhog


@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog_api=mailhog_api)
    return account_helper


@pytest.fixture
def auth_account_helper(mailhog_api, prepare_user_faker):
    dm_api_conf = DmApiConf(host=v.get("service.dm_api_account"))
    account_api = DMApiAccount(dm_api_conf)

    login = prepare_user_faker.login
    password = prepare_user_faker.password
    email = prepare_user_faker.email

    account_helper = AccountHelper(dm_account_api=account_api, mailhog_api=mailhog_api)
    account_helper.register_and_activate_user(login=login, password=password, email=email)
    account_helper.auth_user(login=login, password=password)

    return account_helper


@pytest.fixture
@allure.step("Подготовка данных пользователя для регистрации, генерация фейковых тестовых данных")
def prepare_user_faker():
    login = Faker().user_name()
    password = Faker().password()
    email = Faker().email()

    User = namedtuple("User", ["login", "password", "email"])
    user = User(login, password, email)
    return user


@pytest.fixture
@allure.step("Подготовка данных пользователя для регистрации")
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