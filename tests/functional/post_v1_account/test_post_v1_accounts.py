from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account


def test_post_v1_accounts(account_helper, user_parametrize_test_data):
    login = user_parametrize_test_data['login']
    password = user_parametrize_test_data['password']
    email = user_parametrize_test_data['email']
    expected_status_code = user_parametrize_test_data['expected_status']

    if expected_status_code == 200:
        with check_status_code_http():
            account_helper.register_and_activate_user(login=login, password=password, email=email)
            response = account_helper.user_login(login=login, password=password)
            PostV1Account.check_response_values(login, response)
    else:
        with check_status_code_http(expected_status_code=expected_status_code, expected_message="Validation failed"):
            account_helper.register_and_activate_user(login=login, password=password, email=email)
