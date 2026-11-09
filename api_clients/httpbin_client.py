
from playwright.sync_api import Playwright


class HttpBinClient:

    def __init__(self, playwright: Playwright, token: str = ""):

        headers = {
            "Accept": "application/json"
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.context = playwright.request.new_context(
            base_url="https://httpbin.org",
            extra_http_headers=headers
        )

    def check_authentication(self):
        return self.context.get("/bearer")

    def close(self):
        self.context.dispose()
