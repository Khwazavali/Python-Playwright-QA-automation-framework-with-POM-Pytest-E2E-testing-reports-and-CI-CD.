
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_logout_blocks_protected_page(page: Page):

    # Step 1: Login with valid credentials
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    # Step 2: Verify successful login
    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    expect(
        page.get_by_text("Products", exact=True)
    ).to_be_visible()

    # Step 3: Open the navigation menu
    page.locator("#react-burger-menu-btn").click()

    # Step 4: Click Logout
    page.locator("#logout_sidebar_link").click()

    # Step 5: Verify return to login page
    expect(page).to_have_url("https://www.saucedemo.com/")

    expect(
        page.get_by_placeholder("Username")
    ).to_be_visible()

    # Step 6: Attempt to access the protected page
    page.goto("https://www.saucedemo.com/inventory.html")

    # Step 7: Verify user is redirected to login
    expect(page).to_have_url("https://www.saucedemo.com/")

    # Step 8: Verify login form is displayed
    expect(
        page.get_by_placeholder("Username")
    ).to_be_visible()

    expect(
        page.get_by_placeholder("Password")
    ).to_be_visible()
