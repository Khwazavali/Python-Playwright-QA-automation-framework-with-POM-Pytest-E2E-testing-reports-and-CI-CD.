
import pytest
from decimal import Decimal

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_checkout_financial_integrity(page: Page):

    # Step 1: Log in
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 2: Create reusable page objects
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    # Step 3: Define our test products
    selected_products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light"
    ]

    expected_prices = {}

    # Step 4: Capture inventory prices and add products
    for product_name in selected_products:

        expected_prices[product_name] = (
            inventory_page.get_product_price(product_name)
        )

        inventory_page.add_product_to_cart(product_name)

    inventory_page.verify_cart_count(2)

    # Step 5: Navigate to cart
    inventory_page.open_cart()

    cart_page.verify_item_count(2)

    for product_name in selected_products:
        cart_page.verify_product_present(product_name)

    # Step 6: Start checkout
    cart_page.proceed_to_checkout()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )

    # Step 7: Enter checkout information
    checkout_page.enter_customer_information(
        "Test", "Customer", "75001"
    )

    checkout_page.continue_checkout()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-two.html"
    )

    # Step 8: Verify each product's checkout price
    for product_name, expected_price in expected_prices.items():

        actual_price = checkout_page.get_item_price(
            product_name
        )

        assert actual_price == expected_price, (
            f"{product_name}: expected ${expected_price}, "
            f"actual ${actual_price}"
        )

        item = checkout_page.get_checkout_item(product_name)

        expect(item).to_have_count(1)

        expect(
            item.locator(".cart_quantity")
        ).to_have_text("1")

    # Step 9: Calculate expected subtotal independently
    expected_subtotal = sum(
        expected_prices.values(),
        Decimal("0.00")
    )

    # Step 10: Read actual values from checkout
    actual_subtotal = checkout_page.get_subtotal()
    actual_tax = checkout_page.get_tax()
    actual_total = checkout_page.get_total()

    # Step 11: Verify financial accuracy
    assert actual_subtotal == expected_subtotal, (
        f"Subtotal mismatch: expected ${expected_subtotal}, "
        f"actual ${actual_subtotal}"
    )

    expected_total = expected_subtotal + actual_tax

    assert actual_total == expected_total, (
        f"Total mismatch: expected ${expected_total}, "
        f"actual ${actual_total}"
    )

    
    
@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_error",
    [
        ("", "Customer", "75001", "First Name is required"),
        ("Test", "", "75001", "Last Name is required"),
        ("Test", "Customer", "", "Postal Code is required"),
    ],
    ids=[
        "missing_first_name",
        "missing_last_name",
        "missing_postal_code"
    ]
)
def test_checkout_required_fields(
    page: Page,
    first_name,
    last_name,
    postal_code,
    expected_error
):

    # Step 1: Login
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 2: Add a product
    page.locator(
        "[data-test='add-to-cart-sauce-labs-backpack']"
    ).click()

    expect(
        page.locator(".shopping_cart_badge")
    ).to_have_text("1")

    # Step 3: Open cart
    page.locator(".shopping_cart_link").click()

    # Step 4: Start checkout
    page.get_by_role("button", name="Checkout").click()

    # Step 5: Verify checkout information page
    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )

    # Step 6: Fill checkout information
    page.get_by_placeholder("First Name").fill(first_name)
    page.get_by_placeholder("Last Name").fill(last_name)
    page.get_by_placeholder("Zip/Postal Code").fill(postal_code)

    # Step 7: Submit
    page.get_by_role("button", name="Continue").click()

    # Step 8: Verify the expected validation error
    error_message = page.locator("[data-test='error']")

    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text(expected_error)

    # Step 9: Verify checkout did not continue
    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )

