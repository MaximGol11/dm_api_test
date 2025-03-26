from datetime import datetime
from hamcrest import assert_that, has_property, has_properties, all_of, starts_with, instance_of, equal_to

from checkers.http_checkers import check_status_code_http


def test_post_v1_accounts(account_helper, user_parametrize_test_data):
    login = user_parametrize_test_data['login']
    password = user_parametrize_test_data['password']
    email = user_parametrize_test_data['email']
    expected_status_code = user_parametrize_test_data['expected_status']

    if expected_status_code == 200:
        with check_status_code_http():
            account_helper.register_and_activate_user(login=login, password=password, email=email)
            response = account_helper.user_login(login=login, password=password)
            assert_that(
                response, all_of(
                    has_property("resource", has_property("login", login)),
                    has_property("resource", has_property("registration", instance_of(datetime))),
                    has_property("resource", has_properties(
                        {
                            "rating": has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                }
                            )
                        }
                    ))
                )
            )
    else:
        with check_status_code_http(expected_status_code=expected_status_code, expected_message="Validation failed"):
            account_helper.register_and_activate_user(login=login, password=password, email=email)