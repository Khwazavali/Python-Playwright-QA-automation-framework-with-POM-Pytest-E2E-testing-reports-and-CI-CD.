
from playwright.sync_api import Browser, expect


# A small demonstration application
HTML = """
<h1>Authentication Demo</h1>

<button id="login">Login</button>
<p id="status"></p>

<script>
function updateStatus() {
    const token = localStorage.getItem("demo_token");

    document.querySelector("#status").textContent =
        token ? "Logged in" : "Not logged in";
}

document.querySelector("#login").onclick = () => {
    localStorage.setItem("demo_token", "fake-demo-token");
    updateStatus();
};

updateStatus();
</script>
"""

BASE_URL = "http://auth-demo.test/"


def test_reuse_browser_storage_state(browser: Browser, tmp_path):

    # Step 1: Create the first browser context
    context_a = browser.new_context()

    # Step 2: Mock the demonstration application
    context_a.route(
        BASE_URL,
        lambda route: route.fulfill(
            status=200,
            content_type="text/html",
            body=HTML
        )
    )

    try:
        page_a = context_a.new_page()
        page_a.goto(BASE_URL)

        # Step 3: Perform login
        page_a.get_by_role("button", name="Login").click()

        expect(page_a.locator("#status")).to_have_text(
            "Logged in"
        )

        # Step 4: Save browser storage to a temporary file
        state_file = tmp_path / "auth_state.json"

        context_a.storage_state(path=state_file)

    finally:
        context_a.close()

    # Step 5: Create a NEW context with saved state
    context_b = browser.new_context(
        storage_state=state_file
    )

    context_b.route(
        BASE_URL,
        lambda route: route.fulfill(
            status=200,
            content_type="text/html",
            body=HTML
        )
    )

    try:
        page_b = context_b.new_page()
        page_b.goto(BASE_URL)

        # Step 6: Verify user is already logged in
        expect(page_b.locator("#status")).to_have_text(
            "Logged in"
        )

        print("Authentication state restored successfully")

    finally:
        context_b.close()
