
from playwright.sync_api import Playwright


def test_get_post(playwright: Playwright):

    # Create an API request context
    api_context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )

    try:
        # Send a GET request
        response = api_context.get("/posts/1")

        # Validate response status
        assert response.status == 200

        # Read JSON response
        response_body = response.json()

        # Validate response data
        assert response_body["id"] == 1
        assert response_body["userId"] == 1
        assert "title" in response_body
        assert "body" in response_body

        print("API response:", response_body)

    finally:
        # Release API request resources
        api_context.dispose()


def test_create_post(playwright: Playwright):

    api_context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )

    try:
        payload = {
            "title": "Playwright API Automation",
            "body": "Learning API testing with Python",
            "userId": 1
        }

        response = api_context.post(
            "/posts",
            data=payload
        )

        assert response.status == 201

        response_body = response.json()

        assert response_body["title"] == payload["title"]
        assert response_body["body"] == payload["body"]
        assert response_body["userId"] == payload["userId"]

        print("POST response:", response_body)

    finally:
        api_context.dispose()
        

def test_put_patch_delete_and_not_found(playwright: Playwright):

    api_context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )

    try:
        # 1. PUT: Replace a post
        full_payload = {
            "id": 1,
            "title": "Updated Post",
            "body": "Full replacement",
            "userId": 1
        }

        put_response = api_context.put(
            "/posts/1",
            data=full_payload
        )

        assert put_response.status == 200
        assert put_response.json()["title"] == "Updated Post"
        print("PUT passed")

        # 2. PATCH: Update only the title
        patch_response = api_context.patch(
            "/posts/1",
            data={"title": "Patched Title"}
        )

        assert patch_response.status == 200
        assert patch_response.json()["title"] == "Patched Title"
        print("PATCH passed")

        # 3. DELETE: Request post deletion
        delete_response = api_context.delete("/posts/1")

        assert delete_response.status == 200
        print("DELETE passed")

        # 4. Negative testing: Request a missing post
        missing_response = api_context.get("/posts/999999")

        assert missing_response.status == 404
        print("Negative GET passed: 404")

    finally:
        api_context.dispose()

