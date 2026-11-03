
from playwright.sync_api import Page, expect


def test_login_page_loads(page: Page):

    # Step 1: Open SauceDemo
    page.goto("https://www.saucedemo.com/")

    # Step 2: Verify the username field
    username_field = page.get_by_placeholder("Username")
    expect(username_field).to_be_visible()

    # Step 3: Verify the password field
    password_field = page.get_by_placeholder("Password")
    expect(password_field).to_be_visible()

    # Step 4: Verify the Login button
    login_button = page.get_by_role("button", name="Login")
    expect(login_button).to_be_visible()
