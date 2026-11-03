
# E-Commerce Quality Engineering Framework
### Playwright | Python | Pytest | Page Object Model | CI/CD

An end-to-end browser automation framework built using Python,
Playwright, and Pytest to validate critical e-commerce workflows.

The framework demonstrates functional testing, negative testing,
data-driven testing, browser session isolation, financial validation,
cross-browser testing, and CI/CD integration.

## Tech Stack

- Python
- Playwright
- Pytest
- Page Object Model (POM)
- pytest-html
- GitHub Actions
- Git

## Application Under Test

SauceDemo: https://www.saucedemo.com/

SauceDemo is a public demonstration e-commerce application
used for practicing software testing.

## Test Coverage

| Module | Scenarios |
|---|---|
| Authentication | Valid login, invalid credentials, required fields, locked-out user |
| Cart | Multiple products, removal, quantity and product integrity |
| Checkout | Required fields, product prices, subtotal and total calculations |
| Order Lifecycle | Complete checkout, order confirmation, cart cleanup |
| Checkout Cancellation | Cart preservation and state recovery |
| Session Management | Logout and protected-route navigation |
| Browser Isolation | Independent browser contexts and shopping carts |

## Framework Architecture

```text
playwright-python-ecommerce-qa/
├── .github/
│   └── workflows/
│       └── playwright-tests.yml
├── pages/
│   ├── __init__.py
│   └── login_page.py
├── tests/
│   ├── test_login.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   ├── test_order_lifecycle.py
│   ├── test_checkout_cancellation.py
│   ├── test_session.py
│   └── test_session_isolation.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository.

2. Create a virtual environment:

   py -m venv .venv

3. Activate it on Windows CMD:

   .venv\Scripts\activate.bat

4. Install dependencies:

   python -m pip install -r requirements.txt

5. Install Playwright browsers:

   python -m playwright install

## Run Tests

Run all tests:

    python -m pytest

Run login tests:

    python -m pytest tests/test_login.py

Run using Chromium:

    python -m pytest --browser chromium

Run using Firefox:

    python -m pytest --browser firefox

Run using WebKit:

    python -m pytest --browser webkit

Run across all three browser engines:

    python -m pytest --browser chromium --browser firefox --browser webkit

## Reporting and Debugging

The framework supports:

- HTML execution reports
- JUnit XML results
- Automatic screenshots on failure
- Playwright traces retained on failure
- Trace Viewer for debugging test execution

Generated artifacts are excluded from Git using .gitignore.

## CI/CD

GitHub Actions automatically runs the Chromium test suite
on pushes and pull requests targeting the main branch.

The workflow:

1. Checks out the repository
2. Configures Python
3. Installs dependencies
4. Installs Chromium
5. Executes Pytest tests
6. Uploads reports and failure evidence

## Testing Approach

The framework emphasizes:

- Business-critical workflow validation
- Positive and negative test scenarios
- Data-driven test execution
- Cross-page data consistency
- Session and browser-context isolation
- Reusable Page Object methods
- Actionable failure diagnostics

## Current Limitations

- SauceDemo is a simulated e-commerce application.
- Financial tests verify displayed arithmetic, not real payments.
- Session tests do not prove backend authorization security.
- CI currently executes the Chromium suite.
- Cross-browser CI and additional Page Objects are planned.

## Future Enhancements

- Additional Page Objects for cart, inventory, and checkout
- Reusable Pytest fixtures and test data management
- Cross-browser CI matrix
- API testing against a suitable API-enabled practice application
- Parallel execution
- Test tagging and smoke/regression suites
- Enhanced execution analytics

## Disclaimer

This is an independent QA automation portfolio project
using a publicly accessible demonstration application.
It is not affiliated with Sauce Labs.
```
