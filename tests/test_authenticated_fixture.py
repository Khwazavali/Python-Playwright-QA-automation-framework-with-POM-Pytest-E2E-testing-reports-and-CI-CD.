
from playwright.sync_api import expect


def test_authenticated_user_can_access_inventory(logged_in_page):

    # The fixture has already logged us in

    expect(logged_in_page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    expect(
        logged_in_page.locator(".inventory_item")
    ).to_have_count(6)
