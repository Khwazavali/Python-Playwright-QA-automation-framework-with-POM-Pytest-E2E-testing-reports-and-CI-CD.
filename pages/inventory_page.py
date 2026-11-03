
from decimal import Decimal

from playwright.sync_api import Page, expect


class InventoryPage:

    def __init__(self, page: Page):

        # Store the browser page
        self.page = page

        # Reusable locators
        self.product_cards = page.locator(".inventory_item")

        self.cart_badge = page.locator(
            ".shopping_cart_badge"
        )

        self.cart_link = page.locator(
            ".shopping_cart_link"
        )

    def get_product(self, product_name: str):

        # Find one specific product card
        return self.product_cards.filter(
            has=self.page.get_by_text(
                product_name, exact=True
            )
        )

    def add_product_to_cart(self, product_name: str):

        # Locate the requested product
        product = self.get_product(product_name)

        # Verify exactly one matching product
        expect(product).to_have_count(1)

        # Click its Add to cart button
        product.get_by_role(
            "button", name="Add to cart"
        ).click()

    def get_product_price(self, product_name: str) -> Decimal:

        # Locate the product
        product = self.get_product(product_name)

        expect(product).to_have_count(1)

        # Read displayed price
        price_text = product.locator(
            ".inventory_item_price"
        ).inner_text()

        # Convert "$29.99" into Decimal("29.99")
        return Decimal(price_text.replace("$", "").strip())

    def verify_cart_count(self, expected_count: int):

        if expected_count == 0:
            expect(self.cart_badge).to_have_count(0)
        else:
            expect(self.cart_badge).to_have_text(
                str(expected_count)
            )

    def open_cart(self):

        # Navigate to the cart
        self.cart_link.click()
