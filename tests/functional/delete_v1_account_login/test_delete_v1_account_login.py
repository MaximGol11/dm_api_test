from checkers.http_checkers import check_status_code_http


def test_delete_v1_account_login(auth_account_helper):
    with check_status_code_http():
        auth_account_helper.logout_user()

    with check_status_code_http(401, "User must be authenticated"):
        auth_account_helper.get_user_account(validate_response=False)
