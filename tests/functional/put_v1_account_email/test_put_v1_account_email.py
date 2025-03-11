from faker import Faker
from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from json import loads
import structlog
from restclient.configuration import Configuration as MailhogConf
from restclient.configuration import Configuration as DmApiConf


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


def get_activation_token_by_login(login, response):
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            return user_data['ConfirmationLinkUrl'].split('/')[-1]

    return f"Токен для пользователя {login}, не был получен по почте."


def test_put_v1_accounts_email():
    account_api = AccountApi(dm_api_conf)
    mailhog_api = MailhogApi(mailhog_conf)
    login_api = LoginApi(dm_api_conf)

    login = Faker().user_name()
    password = Faker().password()
    email = Faker().email()
    new_email = Faker().email()

    json_data = {
        "login": login,
        "password": password,
        "email": email
    }

    login_data = {
        "login": login,
        "password": password
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200
    token = get_activation_token_by_login(login, response)
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200

    response = login_api.post_v1_login(json_data=login_data)
    assert response.status_code == 200

    new_email_data = {
        "login": login,
        "email": new_email,
        "password": password
    }

    response = account_api.put_v1_account_email(json_data=new_email_data)
    assert response.status_code == 200

    response = login_api.post_v1_login(json_data=login_data)
    assert response.status_code == 403

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200
    new_token = get_activation_token_by_login(login, response)

    response = account_api.put_v1_account_token(token=new_token)
    assert response.status_code == 200

    response = login_api.post_v1_login(json_data=login_data)
    assert response.status_code == 200