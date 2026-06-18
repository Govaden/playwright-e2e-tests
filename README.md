# 🎭 playwright-pytest-sandbox

A practice repository for learning and experimenting with end-to-end UI test automation using **Playwright** and **pytest**, built against [SauceDemo](https://www.saucedemo.com/).

![Playwright Tests](https://github.com/Govaden/playwright-pytest-sandbox/actions/workflows/playwright.yml/badge.svg)

---

## 📌 About

This repo contains a collection of automated UI tests structured around the **Page Object Model (POM)** pattern. It covers login flows, cart management, and checkout — with parametrized test cases, xfail markers for known broken users, and full tracing/video/screenshot capture on failure.

---

## 🗂️ Project Structure

```
playwright-pytest-sandbox/
├── pages/
│   ├── login_page.py       # LoginPage — locators & actions for the login screen
│   ├── inventory_page.py   # InventoryPage — product listing, sorting, menu, logout
│   ├── cart_page.py        # CartPage — cart items, removal
│   └── checkout_page.py    # CheckoutPage — checkout form, overview, confirmation
├── tests/
│   ├── test_auth.py        # Login (negative/positive) and logout tests
│   ├── test_cart.py        # Add to cart and remove item tests
│   └── test_checkout.py    # End-to-end checkout flow tests
├── conftest.py             # Browser launch args and viewport fixtures
├── pytest.ini              # Pytest configuration
└── requirements.txt        # Dependencies
```

---

## ⚙️ Setup

**1. Clone the repo**
```bash
git clone https://github.com/Govaden/playwright-pytest-sandbox.git
cd playwright-pytest-sandbox
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

## ▶️ Running Tests

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

## 📊 Reports & Artifacts

Configured in `pytest.ini` — generated automatically on each run:

| Artifact | Location |
|---|---|
| HTML report | `reports/html/report.html` |
| Traces (on failure) | `reports/artifacts/` |
| Videos (on failure) | `reports/artifacts/` |
| Screenshots (on failure) | `reports/artifacts/` |

---

## 📦 Dependencies

| Package | Version |
|---|---|
| pytest | 9.0.3 |
| playwright | 1.59.0 |
| pytest-playwright | 0.7.2 |
| pytest-html | 4.2.0 |

---

## 📚 Resources

- [Playwright for Python — Docs](https://playwright.dev/python/docs/intro)
- [pytest-playwright — GitHub](https://github.com/microsoft/playwright-pytest)
- [pytest — Official Docs](https://docs.pytest.org/)
