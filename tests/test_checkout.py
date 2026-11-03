import pytest
from decimal import Decimal

from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def money(text):
    """Extract a currency amount as a precise Decimal."""
    return Decimal(text.split("$")[-1].strip())


def test_checkout_financial_integrity(page: Page):

    # Step 1: Login
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 2: Select two products
    selected_products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light"
    ]

    expected_prices = {}

    for product_name in selected_products:

        product = page.locator(".inventory_item").filter(
            has=page.locator(
                ".inventory_item_name",
                has_text=product_name
            )
        )

        # Read product price before adding it
        price_text = product.locator(
            ".inventory_item_price"
        ).inner_text()

        expected_prices[product_name] = money(price_text)

        product.get_by_role(
            "button", name="Add to cart"
        ).click()

    # Step 3: Verify cart quantity
    expect(
        page.locator(".shopping_cart_badge")
    ).to_have_text("2")

    # Step 4: Open cart
    page.locator(".shopping_cart_link").click()

    expect(page.locator(".cart_item")).to_have_count(2)

    # Step 5: Proceed to checkout
    page.get_by_role("button", name="Checkout").click()

    # Step 6: Enter checkout details
    page.get_by_placeholder("First Name").fill("Test")
    page.get_by_placeholder("Last Name").fill("Customer")
    page.get_by_placeholder("Zip/Postal Code").fill("75001")

    page.get_by_role("button", name="Continue").click()

    # Step 7: Verify each product and its price
    for product_name, expected_price in expected_prices.items():

        item = page.locator(".cart_item").filter(
            has_text=product_name
        )

        expect(item).to_have_count(1)

        actual_price = money(
            item.locator(".inventory_item_price").inner_text()
        )

        assert actual_price == expected_price, (
            f"{product_name}: expected {expected_price}, "
            f"but found {actual_price}"
        )

        expect(
            item.locator(".cart_quantity")
        ).to_have_text("1")

    # Step 8: Calculate the expected subtotal
    expected_subtotal = sum(
        expected_prices.values(), Decimal("0.00")
    )

    # Step 9: Read displayed subtotal
    displayed_subtotal = money(
        page.locator(".summary_subtotal_label").inner_text()
    )

    assert displayed_subtotal == expected_subtotal, (
        f"Subtotal mismatch: expected {expected_subtotal}, "
        f"actual {displayed_subtotal}"
    )

    # Step 10: Read displayed tax
    displayed_tax = money(
        page.locator(".summary_tax_label").inner_text()
    )

    # Step 11: Read displayed total
    displayed_total = money(
        page.locator(".summary_total_label").inner_text()
    )

    # Step 12: Verify total calculation
    expected_total = expected_subtotal + displayed_tax

    assert displayed_total == expected_total, (
        f"Total mismatch: expected {expected_total}, "
        f"actual {displayed_total}"
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

