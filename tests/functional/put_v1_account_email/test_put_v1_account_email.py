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

dm_api_conf = DmApiConf(host="http://5.63.153.31:5051", disable_log=False)
mailhog_conf = MailhogConf(host="http://5.63.153.31:5025")


def test_put_v1_accounts_email():
    account = DMApiAccount(dm_api_conf)
    mailhog = MailHogApi(mailhog_conf)

    login = Faker().user_name()
    password = Faker().password()
    email = Faker().email()
    new_email = Faker().email()

    account_helper = AccountHelper(dm_account_api=account, mailhog_api=mailhog)

    account_helper.register_and_activate_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_user_email(login=login, password=password, new_email=new_email)

    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403

    account_helper.activate_user(login=login)
    account_helper.user_login(login=login, password=password)