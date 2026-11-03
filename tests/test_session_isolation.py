
from playwright.sync_api import Browser, expect
from pages.login_page import LoginPage


def test_two_browser_contexts_have_independent_carts(
    browser: Browser
):

    # Step 1: Create two independent browser contexts
    context_a = browser.new_context()
    context_b = browser.new_context()

    try:
        # Step 2: Create one page in each context
        page_a = context_a.new_page()
        page_b = context_b.new_page()

        # Step 3: Login in Context A
        login_a = LoginPage(page_a)
        login_a.navigate()
        login_a.login("standard_user", "secret_sauce")

        expect(page_a).to_have_url(
            "https://www.saucedemo.com/inventory.html"
        )

        # Step 4: Add Backpack in Context A
        page_a.locator(
            "[data-test='add-to-cart-sauce-labs-backpack']"
        ).click()

        expect(
            page_a.locator(".shopping_cart_badge")
        ).to_have_text("1")

        # Step 5: Login independently in Context B
        login_b = LoginPage(page_b)
        login_b.navigate()
        login_b.login("standard_user", "secret_sauce")

        expect(page_b).to_have_url(
            "https://www.saucedemo.com/inventory.html"
        )

        # Step 6: Verify Context B has no cart badge
        expect(
            page_b.locator(".shopping_cart_badge")
        ).to_have_count(0)

        # Step 7: Verify Context B's cart is empty
        page_b.locator(".shopping_cart_link").click()

        expect(
            page_b.locator(".cart_item")
        ).to_have_count(0)

        # Step 8: Verify Context A still has Backpack
        page_a.locator(".shopping_cart_link").click()

        expect(
            page_a.locator(".cart_item")
        ).to_have_count(1)

        expect(
            page_a.get_by_text(
                "Sauce Labs Backpack", exact=True
            )
        ).to_be_visible()

        # Step 9: Recheck Context B
        expect(
            page_b.locator(".cart_item")
        ).to_have_count(0)

    finally:
        # Step 10: Close both browser contexts
        context_a.close()
        context_b.close()
