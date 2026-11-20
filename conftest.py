import os
from pathlib import Path
import allure
import pytest
from playwright.sync_api import Browser, Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

STANDARD_USER_STATE = Path(__file__).parent / "playwright" / ".auth" / "standard_user.json"

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "slow_mo": 0 if os.getenv("CI") else 500,
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture(scope="session")
def standard_user_state(browser: Browser, browser_context_args) -> Path:
    """Log in as standard_user through the UI once per session and save the storage state."""
    # No video for this setup context; it belongs to no test.
    context_args = {k: v for k, v in browser_context_args.items() if k != "record_video_dir"}
    context = browser.new_context(**context_args)
    try:
        page = context.new_page()
        login = LoginPage(page)
        login.open()
        login.login("standard_user", "secret_sauce")
        expect(page).to_have_url(InventoryPage.URL_PATTERN)
        STANDARD_USER_STATE.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path=STANDARD_USER_STATE)
    finally:
        context.close()
    return STANDARD_USER_STATE

@pytest.fixture
def logged_in_page(new_context, standard_user_state) -> Page:
    """Inventory page in a new context that starts logged in as standard_user."""
    # new_context applies browser_context_args (viewport, base_url) and records traces, videos and screenshots.
    context = new_context(storage_state=standard_user_state)
    page = context.new_page()
    InventoryPage(page).open()
    return page

@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure result when a UI test fails."""
    report = yield
    if report.when != "call" or not report.failed:
        return report

    funcargs = getattr(item, "funcargs", {})
    page = funcargs.get("page") or funcargs.get("logged_in_page")
    if page is None:
        return report

    try:
        allure.attach(
            page.screenshot(full_page=True),
            name="Screenshot on failure",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        # A closed or crashed page must never turn into an extra test error.
        pass
    return report
