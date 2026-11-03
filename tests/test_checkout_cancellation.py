
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_checkout_cancellation_preserves_cart(page: Page):

    # Step 1: Login
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 2: Define products to purchase
    selected_products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light"
    ]

    # Step 3: Add both products to cart
    for name in selected_products:
        product = page.locator(".inventory_item").filter(
            has=page.locator(
                ".inventory_item_name",
                has_text=name
            )
        )

        expect(product).to_have_count(1)

        product.get_by_role(
            "button", name="Add to cart"
        ).click()

    # Step 4: Verify cart badge
    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("2")

    # Step 5: Open shopping cart
    page.locator(".shopping_cart_link").click()

    expect(page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )

    # Step 6: Begin checkout
    page.get_by_role("button", name="Checkout").click()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )

    # Step 7: Enter valid checkout details
    page.get_by_placeholder("First Name").fill("Test")
    page.get_by_placeholder("Last Name").fill("Customer")
    page.get_by_placeholder("Zip/Postal Code").fill("75001")

    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url(
        "https://www.saucedemo.com/checkout-step-two.html"
    )

    # Step 8: Cancel checkout instead of finishing
    page.get_by_role("button", name="Cancel").click()

    # Step 9: Verify return to inventory
    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Step 10: Verify cart badge still shows 2
    expect(cart_badge).to_have_text("2")

    # Step 11: Open cart again
    page.locator(".shopping_cart_link").click()

    # Step 12: Verify original products remain
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

    # Step 13: Verify no order completion page appeared
    expect(page).not_to_have_url(
        "https://www.saucedemo.com/checkout-complete.html"
    )
