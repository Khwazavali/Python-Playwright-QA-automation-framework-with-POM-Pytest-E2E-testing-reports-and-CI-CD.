
from playwright.sync_api import Page, expect


MAIN_HTML = """
<h1>Demo Store</h1>
<a href="http://popup-demo.test/help"
   target="_blank">
    Open Help Center
</a>
"""

HELP_HTML = """
<h1>Help Center</h1>
<p>Welcome to customer support</p>
"""


def test_open_and_switch_tabs(page: Page):

    context = page.context

    # Step 1: Mock the Help Center page
    context.route(
        "http://popup-demo.test/help",
        lambda route: route.fulfill(
            status=200,
            content_type="text/html",
            body=HELP_HTML
        )
    )

    # Step 2: Open main page
    page.set_content(MAIN_HTML)

    expect(
        page.get_by_role("heading", name="Demo Store")
    ).to_be_visible()

    # Step 3: Capture new tab before clicking
    with page.expect_popup() as popup_info:
        page.get_by_role(
            "link", name="Open Help Center"
        ).click()

    popup = popup_info.value

    # Step 4: Verify popup content
    expect(popup).to_have_url(
        "http://popup-demo.test/help"
    )

    expect(
        popup.get_by_role("heading", name="Help Center")
    ).to_be_visible()

    # Step 5: Check number of open tabs
    assert len(context.pages) == 2

    print("Popup opened successfully")

    # Step 6: Close popup
    popup.close()

    assert len(context.pages) == 1

    # Step 7: Continue with original page
    expect(
        page.get_by_role("heading", name="Demo Store")
    ).to_be_visible()

    print("Returned to original page")
