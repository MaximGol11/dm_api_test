from hamcrest import (
    assert_that,
    has_property,
    has_properties,
    all_of,
    equal_to,
    greater_than_or_equal_to,
    contains_inanyorder
)


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.get_user_account()
    assert_that(
        response, all_of(
            has_property("resource", has_property("settings", has_property("color_schema", equal_to("Modern")))),
            has_property("resource", has_property("settings", has_property(
                "paging", has_properties(
                    posts_per_page=greater_than_or_equal_to(10),
                    comments_per_page=greater_than_or_equal_to(10),
                    topics_per_page=greater_than_or_equal_to(10),
                    messages_per_page=greater_than_or_equal_to(10),
                    entities_per_page=greater_than_or_equal_to(10),
                )
            ))),
            has_property("resource", has_property("roles", contains_inanyorder("Guest", "Player")))
        )
    )