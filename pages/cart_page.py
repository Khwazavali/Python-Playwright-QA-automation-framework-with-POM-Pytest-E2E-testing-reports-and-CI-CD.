
from playwright.sync_api import Page, expect


class CartPage:

    def __init__(self, page: Page):

        # Store the browser page
        self.page = page

        # Store reusable cart locators
        self.cart_items = page.locator(".cart_item")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def get_cart_item(self, product_name: str):

        # Find the product row with this exact name
        return self.cart_items.filter(
            has=self.page.get_by_text(
                product_name, exact=True
            )
        )

    def remove_product(self, product_name: str):

        # Locate the requested cart item
        item = self.get_cart_item(product_name)

        expect(item).to_have_count(1)

        # Click Remove inside that item
        item.get_by_role(
            "button", name="Remove"
        ).click()

    def verify_item_count(self, expected_count: int):

        # Verify how many rows appear in the cart
        expect(self.cart_items).to_have_count(expected_count)

    def verify_product_present(self, product_name: str):

        # Verify exactly one matching cart item exists
        expect(
            self.get_cart_item(product_name)
        ).to_have_count(1)

    def verify_product_absent(self, product_name: str):

        # Verify the item no longer exists in the cart
        expect(
            self.get_cart_item(product_name)
        ).to_have_count(0)

    def verify_cart_badge(self, expected_count: int):

        # Badge disappears when cart is empty
        if expected_count == 0:
            expect(self.cart_badge).to_have_count(0)
        else:
            expect(self.cart_badge).to_have_text(
                str(expected_count)
            )

    def proceed_to_checkout(self):

        self.page.get_by_role(
            "button", name="Checkout"
        ).click()
