
import os
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import Page, expect


HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 30px;
            background: white;
        }

        .product {
            width: 300px;
            padding: 20px;
            border: 1px solid #cccccc;
        }

        button {
            background: green;
            color: white;
            padding: 10px;
            border: none;
        }
    </style>
</head>
<body>
    <div class="product">
        <h1>Demo Store</h1>
        <p>Sauce Labs Backpack</p>
        <button>Add to cart</button>
    </div>
</body>
</html>
"""


BASELINE_PATH = (
    Path(__file__).resolve().parent.parent
    / "visual_baselines"
    / "storefront.png"
)


def test_storefront_visual_regression(page: Page):

    # Step 1: Open our controlled HTML page
    page.set_viewport_size({
        "width": 800,
        "height": 600
    })

    page.set_content(HTML)

    expect(
        page.get_by_role("heading", name="Demo Store")
    ).to_be_visible()

    # Step 2: Capture the current screenshot
    screenshot_bytes = page.screenshot(
        animations="disabled"
    )

    # Step 3: Generate baseline only when requested
    if os.getenv("UPDATE_VISUAL_BASELINE") == "1":

        BASELINE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        BASELINE_PATH.write_bytes(screenshot_bytes)

        print("Visual baseline created")
        return

    # Step 4: Make sure the baseline exists
    assert BASELINE_PATH.exists(), (
        "Baseline missing. Generate it first."
    )

    # Step 5: Load both images
    with Image.open(BASELINE_PATH) as baseline_file:
        baseline = baseline_file.convert("RGB")

    with Image.open(BytesIO(screenshot_bytes)) as actual_file:
        actual = actual_file.convert("RGB")

    # Step 6: Compare screenshot dimensions
    assert baseline.size == actual.size, (
        "Screenshot dimensions have changed"
    )

    # Step 7: Compare pixels
    difference = ImageChops.difference(
        baseline,
        actual
    )

    assert difference.getbbox() is None, (
        "Visual regression detected!"
    )

    print("Visual comparison passed")
