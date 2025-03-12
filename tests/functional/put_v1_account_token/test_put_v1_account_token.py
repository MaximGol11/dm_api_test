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


def test_put_v1_accounts_token():
    account = DMApiAccount(dm_api_conf)
    mailhog = MailHogApi(mailhog_conf)

    login = Faker().user_name()
    password = Faker().password()
    email = Faker().email()

    account_helper = AccountHelper(dm_account_api=account, mailhog_api=mailhog)

    login_data = {
        "login": login,
        "password": password
    }

    account_helper.register_user_not_activate(login=login, password=password, email=email)

    # Оставлю проверку на 403 код, думаю потом мы с этим разберемся более красиво
    response = account.login_api.post_v1_login(json_data=login_data)
    assert response.status_code == 403

    account_helper.activate_user(login=login)
    account_helper.user_login(login=login, password=password)