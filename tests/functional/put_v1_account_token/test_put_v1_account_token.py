from checkers.http_checkers import check_status_code_http


def test_put_v1_accounts_token(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    with check_status_code_http():
        account_helper.register_user_not_activate(login=login, password=password, email=email)

    with check_status_code_http(403, "User is inactive. Address the technical support for more details"):
        account_helper.user_login(login=login, password=password, validate_response=False)

    with check_status_code_http():
        account_helper.activate_user(login=login)
        account_helper.user_login(login=login, password=password)