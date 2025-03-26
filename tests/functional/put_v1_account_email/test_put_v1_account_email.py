from checkers.http_checkers import check_status_code_http


def test_put_v1_accounts_email(account_helper, prepare_user_faker):
    login = prepare_user_faker.login
    password = prepare_user_faker.password
    email = prepare_user_faker.email
    new_email = f"new_{email}"

    with check_status_code_http():
        account_helper.register_and_activate_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)
        account_helper.change_user_email(login=login, password=password, new_email=new_email)

    with check_status_code_http(403, "User is inactive. Address the technical support for more details"):
        account_helper.user_login(login=login, password=password, validate_response=False)

    with check_status_code_http():
        account_helper.activate_user(login=login)
        account_helper.user_login(login=login, password=password)