
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_multiple_products_cart_integrity(page: Page):

    # Step 1: Login using our Page Object
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    # Verify successful login
    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 2: Locate the Backpack product
    backpack = page.locator(".inventory_item").filter(
        has_text="Sauce Labs Backpack"
    )

    # Add Backpack to cart
    backpack.get_by_role(
        "button", name="Add to cart"
    ).click()

    # Verify badge count is 1
    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")

    # Step 3: Locate the Bike Light product
    bike_light = page.locator(".inventory_item").filter(
        has_text="Sauce Labs Bike Light"
    )

    # Add Bike Light to cart
    bike_light.get_by_role(
        "button", name="Add to cart"
    ).click()

    # Verify badge count is 2
    expect(cart_badge).to_have_text("2")

    # Step 4: Open the shopping cart
    page.locator(".shopping_cart_link").click()

    # Verify cart page
    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )

    # Step 5: Verify both products exist
    expect(
        page.locator(".cart_item")
    ).to_have_count(2)

    expect(
        page.get_by_text("Sauce Labs Backpack", exact=True)
    ).to_be_visible()

    expect(
        page.get_by_text("Sauce Labs Bike Light", exact=True)
    ).to_be_visible()

    # Step 6: Remove Bike Light
    bike_light_cart = page.locator(".cart_item").filter(
        has_text="Sauce Labs Bike Light"
    )

    bike_light_cart.get_by_role(
        "button", name="Remove"
    ).click()

    # Step 7: Verify cart integrity after removal
    expect(
        page.locator(".cart_item")
    ).to_have_count(1)

    expect(
        page.get_by_text("Sauce Labs Backpack", exact=True)
    ).to_be_visible()

    expect(
        page.get_by_text("Sauce Labs Bike Light", exact=True)
    ).to_have_count(0)

    expect(cart_badge).to_have_text("1")
