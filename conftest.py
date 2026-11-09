
import pytest

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


@pytest.fixture(scope="function")
def logged_in_page(page: Page):

    # SETUP: Runs before the test
    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login(
        "standard_user",
        "secret_sauce"
    )

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    print("\n[SETUP] User logged in successfully")

    # TEST EXECUTION: Give the page to the test
    yield page

    # TEARDOWN: Runs after the test
    print("\n[TEARDOWN] Authenticated test completed")
