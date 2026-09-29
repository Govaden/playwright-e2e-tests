# playwright-e2e-tests

[![Playwright Tests](https://github.com/Govaden/playwright-e2e-tests/actions/workflows/playwright.yml/badge.svg)](https://github.com/Govaden/playwright-e2e-tests/actions/workflows/playwright.yml)

End-to-end UI test suite for [SauceDemo](https://www.saucedemo.com/), built with **Playwright** and **pytest** using the **Page Object Model (POM)**. Covers authentication, cart management, and the checkout flow, with parametrized cases, `xfail` markers for known-broken demo users, and trace/video/screenshot capture on failure.

---

## Project Structure

```
playwright-e2e-tests/
├── pages/
│   ├── login_page.py       # LoginPage — locators & actions for the login screen
│   ├── inventory_page.py   # InventoryPage — product listing, sorting, menu, logout
│   ├── cart_page.py        # CartPage — cart items, removal
│   └── checkout_page.py    # CheckoutPage — checkout form, overview, confirmation
├── tests/
│   ├── test_auth.py        # Login (negative/positive) and logout
│   ├── test_cart.py        # Add-to-cart and remove-item
│   └── test_checkout.py    # End-to-end checkout flow
├── conftest.py             # Browser launch args and viewport fixtures
├── pytest.ini              # Pytest configuration
└── requirements.txt        # Pinned dependencies
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Govaden/playwright-e2e-tests.git
cd playwright-e2e-tests
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
playwright install
```

---

## Running Tests

Run all tests:
```bash
pytest
```

Run a specific test file:
```bash
pytest tests/test_auth.py
```

Run in headed mode (see the browser):
```bash
pytest --headed
```

Run with a specific browser:
```bash
pytest --browser firefox
```

---

## Test Coverage

| Test | File | Scenario |
|---|---|---|
| `test_negative_login` | `test_auth.py` | Login rejection: empty username, missing password, bad credentials, locked-out user |
| `test_positive_login` | `test_auth.py` | Successful login → open product detail → sort Z→A (`error_user`/`problem_user` xfail) |
| `test_logout` | `test_auth.py` | Log in, open menu, log out, return to login page (5 users) |
| `test_cart` | `test_cart.py` | Add multiple items, verify badge count, remove one, verify count and remaining items |
| `test_checkout` | `test_checkout.py` | Full checkout: add item → fill info → overview → finish → confirmation (empty name xfail) |

---

## Known Application Behaviour

| User / Scenario | Expected behaviour | Actual behaviour |
|---|---|---|
| `error_user` — positive login | Lands on inventory page | Wrong product image opens; sort dropdown broken |
| `problem_user` — positive login | Lands on inventory page | Sort dropdown broken; some product images incorrect |
| `performance_glitch_user` — login | Lands on inventory page | Artificial delay causes page title to not appear within assertion timeout in CI |
| `test_checkout` — empty first name | Validation error shown | Form submits without first name; checkout proceeds incorrectly |

These are intentional defects in the SauceDemo application, not bugs in the test suite. Marking them `xfail` keeps CI green while documenting the known broken behaviour clearly.

---

## Reports & Artifacts

Configured in `pytest.ini` — generated automatically on each run:

| Artifact | Location |
|---|---|
| HTML report | `reports/html/report.html` |
| JUnit XML | `reports/junit/results.xml` |
| Traces (on failure) | `reports/artifacts/` |
| Videos (on failure) | `reports/artifacts/` |
| Screenshots (on failure) | `reports/artifacts/` |

---

## Dependencies

| Package | Version |
|---|---|
| pytest | 9.0.3 |
| playwright | 1.59.0 |
| pytest-playwright | 0.7.2 |
| pytest-html | 4.2.0 |

---

## Continuous Integration

GitHub Actions runs the suite on every push and pull request to `main`, plus a nightly scheduled run. See [`.github/workflows/playwright.yml`](.github/workflows/playwright.yml).

---

## Resources

- [Playwright for Python — Docs](https://playwright.dev/python/docs/intro)
- [pytest-playwright — GitHub](https://github.com/microsoft/playwright-pytest)
- [pytest — Official Docs](https://docs.pytest.org/)
