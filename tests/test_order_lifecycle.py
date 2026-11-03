
from decimal import Decimal

from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def read_money(text: str) -> Decimal:
    return Decimal(text.split("$")[-1].strip())


def test_complete_order_lifecycle(page: Page):

    # Step 1: Log in
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 2: Select products and capture expected prices
    selected_products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light"
    ]

    expected_prices = {}

    for name in selected_products:
        product = page.locator(".inventory_item").filter(
            has=page.locator(
                ".inventory_item_name",
                has_text=name
            )
        )

        expect(product).to_have_count(1)

        price_text = product.locator(
            ".inventory_item_price"
        ).inner_text()

        expected_prices[name] = read_money(price_text)

        product.get_by_role(
            "button", name="Add to cart"
        ).click()

    # Step 3: Verify cart badge
    expect(
        page.locator(".shopping_cart_badge")
    ).to_have_text("2")

    # Step 4: Open cart and validate items
    page.locator(".shopping_cart_link").click()

    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )

    expect(page.locator(".cart_item")).to_have_count(2)

    for name in selected_products:
        item = page.locator(".cart_item").filter(
            has=page.locator(
                ".inventory_item_name",
                has_text=name
            )
        )

        expect(item).to_have_count(1)
        expect(item.locator(".cart_quantity")).to_have_text("1")

    # Step 5: Begin checkout
    page.get_by_role("button", name="Checkout").click()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )

    # Step 6: Provide customer information
    page.get_by_placeholder("First Name").fill("Test")
    page.get_by_placeholder("Last Name").fill("Customer")
    page.get_by_placeholder("Zip/Postal Code").fill("75001")

    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-two.html"
    )

    # Step 7: Validate checkout items and prices
    for name, expected_price in expected_prices.items():
        item = page.locator(".cart_item").filter(
            has=page.locator(
                ".inventory_item_name",
                has_text=name
            )
        )

        expect(item).to_have_count(1)
        expect(item.locator(".cart_quantity")).to_have_text("1")

        actual_price = read_money(
            item.locator(".inventory_item_price").inner_text()
        )

        assert actual_price == expected_price, (
            f"{name}: expected ${expected_price}, "
            f"actual ${actual_price}"
        )

    # Step 8: Verify financial integrity
    expected_subtotal = sum(
        expected_prices.values(), Decimal("0.00")
    )

    actual_subtotal = read_money(
        page.locator(".summary_subtotal_label").inner_text()
    )

    assert actual_subtotal == expected_subtotal

    displayed_tax = read_money(
        page.locator(".summary_tax_label").inner_text()
    )

    displayed_total = read_money(
        page.locator(".summary_total_label").inner_text()
    )

    assert displayed_total == expected_subtotal + displayed_tax, (
        "Checkout total does not match subtotal plus tax"
    )

    # Step 9: Complete the order
    page.get_by_role("button", name="Finish").click()

    # Step 10: Verify order confirmation
    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-complete.html"
    )

    expect(
        page.get_by_text(
            "Thank you for your order!", exact=True
        )
    ).to_be_visible()

    # Step 11: Verify cart is cleared
    expect(
        page.locator(".shopping_cart_badge")
    ).to_have_count(0)

    page.locator(".shopping_cart_link").click()

    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )

    expect(
        page.locator(".cart_item")
    ).to_have_count(0)
