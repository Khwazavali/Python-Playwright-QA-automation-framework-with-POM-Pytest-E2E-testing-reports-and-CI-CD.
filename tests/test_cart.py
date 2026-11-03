
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_multiple_products_cart_integrity(page: Page):

    # Step 1: Login
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 2: Create InventoryPage object
    inventory_page = InventoryPage(page)

    # Step 3: Add Backpack
    inventory_page.add_product_to_cart(
        "Sauce Labs Backpack"
    )

    inventory_page.verify_cart_count(1)

    # Step 4: Add Bike Light
    inventory_page.add_product_to_cart(
        "Sauce Labs Bike Light"
    )

    inventory_page.verify_cart_count(2)

    # Step 5: Open cart
    inventory_page.open_cart()

    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )

    # Step 6: Verify both products are present
    expect(page.locator(".cart_item")).to_have_count(2)

    expect(
        page.get_by_text(
            "Sauce Labs Backpack", exact=True
        )
    ).to_be_visible()

    expect(
        page.get_by_text(
            "Sauce Labs Bike Light", exact=True
        )
    ).to_be_visible()

    # Step 7: Remove Bike Light
    bike_light = page.locator(".cart_item").filter(
        has_text="Sauce Labs Bike Light"
    )

    bike_light.get_by_role(
        "button", name="Remove"
    ).click()

    # Step 8: Verify cart after removal
    expect(page.locator(".cart_item")).to_have_count(1)

    expect(
        page.get_by_text(
            "Sauce Labs Backpack", exact=True
        )
    ).to_be_visible()

    expect(
        page.get_by_text(
            "Sauce Labs Bike Light", exact=True
        )
    ).to_have_count(0)

    inventory_page.verify_cart_count(1)
