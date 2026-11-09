
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_checkout_cancellation_preserves_cart(logged_in_page):

    # Login is completed automatically by the fixture
    page = logged_in_page

    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    selected_products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light"
    ]

    # Step 1: Add products
    for product_name in selected_products:
        inventory_page.add_product_to_cart(product_name)

    inventory_page.verify_cart_count(2)

    # Step 2: Open cart
    inventory_page.open_cart()

    cart_page.verify_item_count(2)

    # Step 3: Begin checkout
    cart_page.proceed_to_checkout()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )

    # Step 4: Enter customer information
    checkout_page.enter_customer_information(
        "Test", "Customer", "75001"
    )

    checkout_page.continue_checkout()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-two.html"
    )

    # Step 5: Cancel checkout
    checkout_page.cancel_checkout()

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 6: Verify cart remains unchanged
    inventory_page.verify_cart_count(2)

    inventory_page.open_cart()

    cart_page.verify_item_count(2)

    for product_name in selected_products:
        cart_page.verify_product_present(product_name)

        item = cart_page.get_cart_item(product_name)

        expect(
            item.locator(".cart_quantity")
        ).to_have_text("1")
