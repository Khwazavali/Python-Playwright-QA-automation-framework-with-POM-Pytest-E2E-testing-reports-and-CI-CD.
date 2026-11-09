
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_checkout_cancellation_preserves_cart(page: Page):

    # Step 1: Login
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 2: Create Page Object instances
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    # Step 3: Select products
    selected_products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light"
    ]

    for product_name in selected_products:
        inventory_page.add_product_to_cart(product_name)

    inventory_page.verify_cart_count(2)

    # Step 4: Open cart
    inventory_page.open_cart()

    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )

    cart_page.verify_item_count(2)

    # Step 5: Begin checkout
    cart_page.proceed_to_checkout()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )

    # Step 6: Complete customer information
    checkout_page.enter_customer_information(
        "Test", "Customer", "75001"
    )

    checkout_page.continue_checkout()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-two.html"
    )

    # Step 7: Cancel from the checkout overview
    checkout_page.cancel_checkout()

    # SauceDemo returns to inventory after cancellation
    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 8: Verify cart badge still shows two products
    inventory_page.verify_cart_count(2)

    # Step 9: Reopen the cart
    inventory_page.open_cart()

    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )

    # Step 10: Verify products were preserved
    cart_page.verify_item_count(2)

    for product_name in selected_products:
        cart_page.verify_product_present(product_name)

        item = cart_page.get_cart_item(product_name)

        expect(
            item.locator(".cart_quantity")
        ).to_have_text("1")
