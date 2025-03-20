from datetime import datetime
from hamcrest import assert_that, has_property, has_properties, all_of, starts_with, instance_of, equal_to


def test_post_v1_accounts(account_helper, prepare_user_faker):
    login = prepare_user_faker.login
    password = prepare_user_faker.password
    email = prepare_user_faker.email

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
