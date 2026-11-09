
from playwright.sync_api import Playwright

from api_clients.httpbin_client import HttpBinClient


def test_bearer_authentication(playwright: Playwright):

    # This is a fake token for demonstration only
    client = HttpBinClient(
        playwright,
        token="practice-token"
    )

    try:
        response = client.check_authentication()

        assert response.status == 200

        response_body = response.json()

        assert response_body["authenticated"] is True

        print("Bearer token accepted")

    finally:
        client.close()


def test_missing_bearer_token(playwright: Playwright):

    client = HttpBinClient(playwright)

    try:
        response = client.check_authentication()

        assert response.status == 401

        print("Missing token rejected")

    finally:
        client.close()
