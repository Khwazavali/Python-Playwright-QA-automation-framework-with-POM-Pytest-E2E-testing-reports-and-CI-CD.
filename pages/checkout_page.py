
from decimal import Decimal

from playwright.sync_api import Page


class CheckoutPage:

    def __init__(self, page: Page):
        self.page = page

        # Checkout information fields
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.postal_code_input = page.get_by_placeholder(
            "Zip/Postal Code"
        )

        # Checkout buttons
        self.continue_button = page.get_by_role(
            "button", name="Continue"
        )
        self.finish_button = page.get_by_role(
            "button", name="Finish"
        )
        self.cancel_button = page.get_by_role(
            "button", name="Cancel"
        )

        # Financial summary labels
        self.subtotal_label = page.locator(
            ".summary_subtotal_label"
        )
        self.tax_label = page.locator(
            ".summary_tax_label"
        )
        self.total_label = page.locator(
            ".summary_total_label"
        )

        # Checkout items and validation messages
        self.checkout_items = page.locator(".cart_item")
        self.error_message = page.locator("[data-test='error']")

    def enter_customer_information(
        self,
        first_name: str,
        last_name: str,
        postal_code: str
    ):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_checkout(self):
        self.continue_button.click()

    def finish_order(self):
        self.finish_button.click()

    def cancel_checkout(self):
        self.cancel_button.click()

    def get_checkout_item(self, product_name: str):
        return self.checkout_items.filter(
            has=self.page.locator(
                ".inventory_item_name",
                has_text=product_name
            )
        )

    def get_item_price(self, product_name: str) -> Decimal:
        item = self.get_checkout_item(product_name)

        price_text = item.locator(
            ".inventory_item_price"
        ).inner_text()

        return self.parse_money(price_text)

    @staticmethod
    def parse_money(text: str) -> Decimal:
        return Decimal(text.split("$")[-1].strip())

    def get_subtotal(self) -> Decimal:
        return self.parse_money(
            self.subtotal_label.inner_text()
        )

    def get_tax(self) -> Decimal:
        return self.parse_money(
            self.tax_label.inner_text()
        )

    def get_total(self) -> Decimal:
        return self.parse_money(
            self.total_label.inner_text()
        )
