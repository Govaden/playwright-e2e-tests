import re
from playwright.sync_api import Page, expect
import pytest
from pytest_playwright.pytest_playwright import page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# performance_glitch_user blocks the browser for 5 s on every inventory render,
# which equals Playwright's default 5 s expect timeout. 15 s allows two renders plus CI margin.
INVENTORY_RENDER_TIMEOUT = 15_000

@pytest.mark.parametrize("username, password, expected_error", [
    ("",              "",             "Epic sadface: Username is required"),
    ("test_user",     "",             "Epic sadface: Password is required"),
    ("standard_user", "12345",        "Epic sadface: Username and password do not match any user in this service"),
    ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
])

def test_negative_login(page: Page, username, password, expected_error):
    login = LoginPage(page)

    login.open()
    login.login(username, password)

    expect(login.error_message(expected_error)).to_be_visible()
    expect(login.accepted_usernames_heading).to_be_visible()
    expect(login.password_for_all_users_heading).to_be_visible()
    expect(login.username_input).to_have_value(username)
    expect(login.password_input).to_have_value(password)
    expect(login.login_button).to_be_visible()

    page.screenshot(path="test_results/test_auth/screenshot_negative_login.png")

@pytest.mark.parametrize("username, password", [
    ("standard_user",  "secret_sauce"),
    ("visual_user", "secret_sauce"),
    pytest.param("error_user", "secret_sauce", marks=pytest.mark.xfail(strict=True, reason="Known site bug: error_user cannot sort products; selecting a sort option shows an error alert and the dropdown does not change")),
    pytest.param("problem_user",   "secret_sauce", marks=pytest.mark.xfail(strict=True, reason="Known site bug: problem_user opens the wrong product detail page from the inventory list")),
    ("performance_glitch_user", "secret_sauce"),
])

def test_positive_login(page: Page, username, password):
    login = LoginPage(page)
    inventory = InventoryPage(page)

    login.open()
    login.fill_username(username)
    expect(login.username_input).to_have_value(username)

    login.fill_password(password)
    expect(login.password_input).to_have_value(password)

    login.login_button.hover()
    login.submit()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html", timeout=INVENTORY_RENDER_TIMEOUT)
    expect(inventory.page_title).to_have_text("Products", timeout=INVENTORY_RENDER_TIMEOUT)

    inventory.open_product("Sauce Labs Backpack")
    expect(page).to_have_url(re.compile(r".*inventory-item.*"))
    expect(inventory.item_details_name).to_have_text("Sauce Labs Backpack")

    page.go_back()

    inventory.sort_products("za")  # Sort Z → A
    expect(inventory.sort_dropdown).to_have_value("za", timeout=INVENTORY_RENDER_TIMEOUT)

    page.screenshot(path="test_results/test_auth/screenshot_positive_login.png")

@pytest.mark.parametrize("username, password", [
    ("standard_user",  "secret_sauce"),
    ("problem_user",   "secret_sauce"),
    ("error_user", "secret_sauce"),
    ("visual_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce"),
])

def test_logout(page: Page, username, password):
    login = LoginPage(page)
    inventory = InventoryPage(page)

    login.open()
    login.fill_username(username)
    expect(login.username_input).to_have_value(username)

    login.fill_password(password)
    expect(login.password_input).to_have_value(password)

    login.submit()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html", timeout=INVENTORY_RENDER_TIMEOUT)
    expect(inventory.inventory_list).to_be_visible(timeout=INVENTORY_RENDER_TIMEOUT)

    inventory.open_menu()
    expect(inventory.menu_wrapper).to_have_attribute("aria-hidden", "false")
    expect(inventory.logout_sidebar_link).to_be_visible()
    
    inventory.logout()

    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(login.username_input).to_be_visible()
    expect(login.password_input).to_be_visible()
    expect(login.login_button).to_be_visible()

    page.screenshot(path="test_results/test_auth/screenshot_logout.png")