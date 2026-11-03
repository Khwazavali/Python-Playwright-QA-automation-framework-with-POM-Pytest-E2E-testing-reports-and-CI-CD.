
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def test_multiple_products_cart_integrity(page: Page):

    # Step 1: Login
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 2: Create page objects
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

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

    # Step 5: Open shopping cart
    inventory_page.open_cart()

    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )

    # Step 6: Verify both products
    cart_page.verify_item_count(2)
    cart_page.verify_product_present("Sauce Labs Backpack")
    cart_page.verify_product_present("Sauce Labs Bike Light")

    # Step 7: Remove Bike Light
    cart_page.remove_product("Sauce Labs Bike Light")

    # Step 8: Verify remaining cart state
    cart_page.verify_item_count(1)
    cart_page.verify_product_present("Sauce Labs Backpack")
    cart_page.verify_product_absent("Sauce Labs Bike Light")
    cart_page.verify_cart_badge(1)
