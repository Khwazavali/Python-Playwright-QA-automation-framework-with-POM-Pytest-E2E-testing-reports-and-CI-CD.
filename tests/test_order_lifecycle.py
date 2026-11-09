
from decimal import Decimal

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_complete_order_lifecycle(page: Page):

    # Step 1: Login
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 2: Initialize our Page Objects
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    # Step 3: Select products and capture their prices
    selected_products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light"
    ]

    expected_prices = {}

    for product_name in selected_products:
        expected_prices[product_name] = (
            inventory_page.get_product_price(product_name)
        )

        inventory_page.add_product_to_cart(product_name)

    inventory_page.verify_cart_count(2)

    # Step 4: Verify the shopping cart
    inventory_page.open_cart()

    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )

    cart_page.verify_item_count(2)

    for product_name in selected_products:
        cart_page.verify_product_present(product_name)

        item = cart_page.get_cart_item(product_name)
        expect(item.locator(".cart_quantity")).to_have_text("1")

    # Step 5: Proceed to checkout
    cart_page.proceed_to_checkout()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )

    # Step 6: Enter customer information
    checkout_page.enter_customer_information(
        "Test", "Customer", "75001"
    )

    checkout_page.continue_checkout()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-two.html"
    )

    # Step 7: Verify product details at checkout
    for product_name, expected_price in expected_prices.items():

        item = checkout_page.get_checkout_item(product_name)

        expect(item).to_have_count(1)

        expect(item.locator(".cart_quantity")).to_have_text("1")

        actual_price = checkout_page.get_item_price(product_name)

        assert actual_price == expected_price, (
            f"Price mismatch for {product_name}: "
            f"expected ${expected_price}, "
            f"actual ${actual_price}"
        )

    # Step 8: Independently calculate expected subtotal
    expected_subtotal = sum(
        expected_prices.values(),
        Decimal("0.00")
    )

    actual_subtotal = checkout_page.get_subtotal()
    actual_tax = checkout_page.get_tax()
    actual_total = checkout_page.get_total()

    assert actual_subtotal == expected_subtotal, (
        f"Subtotal mismatch: expected ${expected_subtotal}, "
        f"actual ${actual_subtotal}"
    )

    assert actual_total == expected_subtotal + actual_tax, (
        "Checkout total does not match subtotal plus tax"
    )

    # Step 9: Complete the order
    checkout_page.finish_order()

    # Step 10: Verify order confirmation
    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-complete.html"
    )

    expect(
        page.get_by_text("Thank you for your order!", exact=True)
    ).to_be_visible()

    # Step 11: Verify cart is cleared after completion
    cart_page.verify_cart_badge(0)

    page.locator(".shopping_cart_link").click()

    cart_page.verify_item_count(0)
