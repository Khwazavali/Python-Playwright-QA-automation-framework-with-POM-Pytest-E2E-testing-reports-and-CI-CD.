
import pytest

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


@pytest.mark.smoke
def test_smoke_login(page: Page):

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )


@pytest.mark.regression
def test_regression_invalid_login(page: Page):

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("invalid_user", "wrong_password")

    expect(login_page.error_message).to_be_visible()


@pytest.mark.regression
@pytest.mark.critical
def test_critical_cart_access(logged_in_page):

    page = logged_in_page

    page.locator(".shopping_cart_link").click()

    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )
