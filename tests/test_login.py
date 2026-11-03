
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


# TC_LOGIN_002: Successful Login
def test_successful_login(page: Page):

    login_page = LoginPage(page)
    login_page.navigate()

    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    expect(
        page.get_by_text("Products", exact=True)
    ).to_be_visible()


# TC_LOGIN_003: Invalid Credentials
def test_invalid_login(page: Page):

    login_page = LoginPage(page)
    login_page.navigate()

    login_page.login("invalid_user", "wrong_password")

    expect(login_page.error_message).to_contain_text(
        "Username and password do not match"
    )

    expect(page).to_have_url("https://www.saucedemo.com/")


# TC_LOGIN_004: Empty Username
def test_login_with_empty_username(page: Page):

    login_page = LoginPage(page)
    login_page.navigate()

    login_page.login("", "secret_sauce")

    expect(login_page.error_message).to_contain_text(
        "Username is required"
    )

    expect(page).to_have_url("https://www.saucedemo.com/")


# TC_LOGIN_005: Empty Password
def test_login_with_empty_password(page: Page):

    login_page = LoginPage(page)
    login_page.navigate()

    login_page.login("standard_user", "")

    expect(login_page.error_message).to_contain_text(
        "Password is required"
    )

    expect(page).to_have_url("https://www.saucedemo.com/")


# TC_LOGIN_006: Locked-Out User
def test_locked_out_user(page: Page):

    login_page = LoginPage(page)
    login_page.navigate()

    login_page.login("locked_out_user", "secret_sauce")

    expect(login_page.error_message).to_contain_text(
        "Sorry, this user has been locked out."
    )

    expect(page).to_have_url("https://www.saucedemo.com/")
