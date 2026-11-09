
from playwright.sync_api import Page, expect


def test_file_upload(page: Page, tmp_path):

    # Step 1: Create a sample CSV file
    file_path = tmp_path / "products.csv"

    csv_data = "id,name\n1,Backpack\n2,Bike Light\n"

    file_path.write_text(
        csv_data,
        encoding="utf-8"
    )

    # Step 2: Create a simple upload form
    page.set_content("""
        <h1>File Upload Demo</h1>

        <label for="file-upload">Upload CSV</label>
        <input type="file" id="file-upload">
    """)

    # Step 3: Select the CSV file
    upload_input = page.get_by_label("Upload CSV")

    upload_input.set_input_files(file_path)

    # Step 4: Verify the selected filename
    expect(upload_input).to_have_js_property(
        "value",
        "C:\\fakepath\\products.csv"
    )

    # Step 5: Read the selected file contents
    uploaded_content = upload_input.evaluate(
        "(element) => element.files[0].text()"
    )

    assert uploaded_content.splitlines() == csv_data.splitlines()

    print("File upload selection verified")


def test_file_download(page: Page, tmp_path):

    # Step 1: Create a small download page
    page.set_content("""
        <h1>File Download Demo</h1>

        <a href="https://files-demo.test/report.csv">
            Download Report
        </a>
    """)

    # Step 2: Mock the downloadable CSV response
    csv_data = "id,name\n1,Backpack\n2,Bike Light\n"

    page.route(
        "https://files-demo.test/report.csv",
        lambda route: route.fulfill(
            status=200,
            content_type="text/csv",
            headers={
                "Content-Disposition":
                    'attachment; filename="report.csv"'
            },
            body=csv_data
        )
    )

    # Step 3: Wait for the download while clicking
    with page.expect_download() as download_info:
        page.get_by_role(
            "link", name="Download Report"
        ).click()

    download = download_info.value

    # Step 4: Verify the suggested filename
    assert download.suggested_filename == "report.csv"

    # Step 5: Save the file temporarily
    saved_file = tmp_path / download.suggested_filename

    download.save_as(saved_file)

    # Step 6: Validate the downloaded file
    assert saved_file.exists()

    assert saved_file.read_text(
        encoding="utf-8"
    ) == csv_data

    print("File download verified")
