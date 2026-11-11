import allure
from playwright.sync_api import Page, expect
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.mark.parametrize("first_name, last_name, postal_code", [
    ("John", "Doe", "12345"),
    ("Jane", "Smith", "54321"),
])

@allure.title("Complete checkout with postal code {postal_code}")
def test_checkout(page: Page, first_name: str, last_name: str, postal_code: str):
    login = LoginPage(page)
    inventory = InventoryPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)

    login.open()
    login.login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(inventory.inventory_list).to_be_visible()

    product = inventory.get_product_item("Sauce Labs Backpack")
    expect(product).to_be_visible()
    inventory.add_product_to_cart("Sauce Labs Backpack")

    expect(cart.cart_badge).to_have_text("1")

    inventory.open_cart()
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    expect(cart.get_product_item("Sauce Labs Backpack")).to_be_visible()

    checkout.go_to_checkout()
    expect(page).to_have_url(CheckoutPage.URL_STEP_ONE)

    checkout.fill_information(first_name, last_name, postal_code)
    expect(checkout.first_name_input).to_have_value(first_name)
    expect(checkout.last_name_input).to_have_value(last_name)
    expect(checkout.postal_code_input).to_have_value(postal_code)

    checkout.continue_checkout()
    expect(page).to_have_url(CheckoutPage.URL_STEP_TWO)

    expect(checkout.get_overview_item("Sauce Labs Backpack")).to_be_visible()
    expect(checkout.summary_total).to_be_visible()

    checkout.finish_checkout()
    expect(page).to_have_url(CheckoutPage.URL_COMPLETE)
    expect(checkout.confirmation_message).to_be_visible()

    page.screenshot(path="test_results/test_checkout/screenshot_checkout.png")

@pytest.mark.parametrize("first_name, last_name, postal_code, expected_error", [
    ("", "Doe", "12345", "Error: First Name is required"),
    ("John", "", "12345", "Error: Last Name is required"),
    ("John", "Doe", "", "Error: Postal Code is required"),
])

@allure.title("Checkout error: {expected_error}")
def test_checkout_missing_required_field(page: Page, first_name: str, last_name: str, postal_code: str, expected_error: str):
    login = LoginPage(page)
    inventory = InventoryPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)

    login.open()
    login.login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(inventory.inventory_list).to_be_visible()

    inventory.add_product_to_cart("Sauce Labs Backpack")
    expect(cart.cart_badge).to_have_text("1")

    inventory.open_cart()
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    checkout.go_to_checkout()
    expect(page).to_have_url(CheckoutPage.URL_STEP_ONE)

    checkout.fill_information(first_name, last_name, postal_code)
    checkout.continue_checkout()

    expect(checkout.error_message).to_have_text(expected_error)
    expect(page).to_have_url(CheckoutPage.URL_STEP_ONE)

    page.screenshot(path="test_results/test_checkout/screenshot_checkout_validation.png")