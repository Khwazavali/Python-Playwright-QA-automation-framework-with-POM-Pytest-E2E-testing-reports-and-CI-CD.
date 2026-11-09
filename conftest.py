
import pytest

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


@pytest.fixture
def logged_in_page(page: Page) -> Page:

    # Create LoginPage using Pytest's browser page
    login_page = LoginPage(page)

    # Open the application
    login_page.navigate()

    # Log in as the standard test user
    login_page.login("standard_user", "secret_sauce")

    # Verify login succeeded before returning the page
    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Give the authenticated page to the test
    return page
