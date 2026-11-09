
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def test_multiple_products_cart_integrity(logged_in_page):

    # The logged_in_page fixture has already completed login
    page = logged_in_page

    # Step 1: Create Page Objects
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    # Step 2: Add Backpack
    inventory_page.add_product_to_cart(
        "Sauce Labs Backpack"
    )

    inventory_page.verify_cart_count(1)

    # Step 3: Add Bike Light
    inventory_page.add_product_to_cart(
        "Sauce Labs Bike Light"
    )

    inventory_page.verify_cart_count(2)

    # Step 4: Open cart
    inventory_page.open_cart()

    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )

    # Step 5: Verify products
    cart_page.verify_item_count(2)
    cart_page.verify_product_present("Sauce Labs Backpack")
    cart_page.verify_product_present("Sauce Labs Bike Light")

    # Step 6: Remove Bike Light
    cart_page.remove_product("Sauce Labs Bike Light")

    # Step 7: Verify final state
    cart_page.verify_item_count(1)
    cart_page.verify_product_present("Sauce Labs Backpack")
    cart_page.verify_product_absent("Sauce Labs Bike Light")
    cart_page.verify_cart_badge(1)
