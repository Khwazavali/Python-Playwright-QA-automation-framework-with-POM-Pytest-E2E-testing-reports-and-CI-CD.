
from playwright.sync_api import Page, expect
from axe_playwright_python.sync_playwright import Axe


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Accessible Demo Store</title>
</head>
<body>
    <main>
        <h1>Demo Store</h1>

        <label for="username">Username</label>
        <input id="username" type="text">

        <button id="login">Login</button>

        <p id="message" role="status"></p>
    </main>

    <script>
        document.querySelector("#login").onclick = () => {
            document.querySelector("#message").textContent =
                "Login button activated";
        };
    </script>
</body>
</html>
"""


def test_accessibility_checks(page: Page):

    # Step 1: Serve our controlled demo page
    page.route(
        "http://accessibility-demo.test/",
        lambda route: route.fulfill(
            status=200,
            content_type="text/html",
            body=HTML
        )
    )

    page.goto("http://accessibility-demo.test/")

    # Step 2: Verify accessible labels
    username = page.get_by_role(
        "textbox", name="Username"
    )

    login_button = page.get_by_role(
        "button", name="Login"
    )

    expect(username).to_be_visible()
    expect(login_button).to_be_visible()

    # Step 3: Verify keyboard navigation
    page.keyboard.press("Tab")
    expect(username).to_be_focused()

    page.keyboard.press("Tab")
    expect(login_button).to_be_focused()

    # Step 4: Activate button using keyboard
    page.keyboard.press("Enter")

    expect(
        page.get_by_role("status")
    ).to_have_text("Login button activated")

    # Step 5: Run automated accessibility scan
    axe = Axe()
    results = axe.run(page)

    print(
        "Accessibility violations:",
        results.violations_count
    )

    # Step 6: Verify no detected violations
    assert results.violations_count == 0, (
        str(results.response.get("violations", []))
    )
