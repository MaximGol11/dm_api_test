from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


def test_get_v1_account_non_auth(account_helper):
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.get_user_account(validate_response=False)


def test_get_v1_account_auth(auth_account_helper):
    with check_status_code_http():
        response = auth_account_helper.get_user_account()
    GetV1Account.check_response_values(response)


