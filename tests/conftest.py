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
    mailhog_conf = MailhogConf(host="http://5.63.153.31:5025")
    mailhog = MailHogApi(mailhog_conf)
    return mailhog


@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog_api=mailhog_api)
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