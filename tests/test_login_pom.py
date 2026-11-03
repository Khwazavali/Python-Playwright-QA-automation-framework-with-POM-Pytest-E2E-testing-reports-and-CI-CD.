
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_successful_login_using_pom(page: Page):

    # Step 1: Create a LoginPage object
    login_page = LoginPage(page)

    # Step 2: Open SauceDemo
    login_page.navigate()

    # Step 3: Enter login credentials
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")

    # Step 4: Submit the login form
    login_page.click_login()

    # Step 5: Verify successful login
    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    expect(
        page.get_by_text("Products", exact=True)
    ).to_be_visible()
