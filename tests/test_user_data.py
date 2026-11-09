
import pytest

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

from test_data.users import (
    STANDARD_USER,
    LOCKED_OUT_USER
)


@pytest.mark.parametrize(
    "user, expected_success",
    [
        (STANDARD_USER, True),
        (LOCKED_OUT_USER, False)
    ],
    ids=["standard_user", "locked_out_user"]
)
def test_login_using_user_data(
    page: Page,
    user: dict,
    expected_success: bool
):

    login_page = LoginPage(page)
    login_page.navigate()

    login_page.login(
        user["username"],
        user["password"]
    )

    if expected_success:
        expect(page).to_have_url(
            "https://www.saucedemo.com/inventory.html"
        )
    else:
        expect(login_page.error_message).to_contain_text(
            "Sorry, this user has been locked out."
        )
