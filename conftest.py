import os
import allure
import pytest

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

@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure result when a UI test fails."""
    report = yield
    if report.when != "call" or not report.failed:
        return report

    page = getattr(item, "funcargs", {}).get("page")
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
