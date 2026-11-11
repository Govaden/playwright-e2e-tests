import allure
from playwright.sync_api import Page, expect
import pytest
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.parametrize("products_to_add, product_to_remove", [
    (
        ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"],
        "Sauce Labs Bike Light"
      ),
    (
        ["Sauce Labs Fleece Jacket", "Sauce Labs Onesie"],
        "Sauce Labs Onesie"
      ),
    (
        ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket"],
        "Sauce Labs Backpack"
      )
])

@allure.title("Add items to cart and remove {product_to_remove}")
def test_cart(page: Page, products_to_add, product_to_remove):
    login = LoginPage(page)
    inventory = InventoryPage(page)
    cart = CartPage(page)

    login.open()
    login.login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(inventory.inventory_list).to_be_visible()

    for product_name in products_to_add:
        inventory.add_product_to_cart(product_name)

    expect(cart.cart_badge).to_have_text(str(len(products_to_add)))

    inventory.open_cart()
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    
    for product_name in products_to_add:
        expect(cart.get_product_item(product_name)).to_be_visible()

    cart.remove_item(product_to_remove)

    expect(cart.get_product_item(product_to_remove)).not_to_be_visible()
    expect(cart.cart_badge).to_have_text(str(len(products_to_add) - 1))

    for product_name in products_to_add:
        if product_name != product_to_remove:
            expect(cart.get_product_item(product_name)).to_be_visible()

    page.screenshot(path="test_results/test_cart/screenshot_cart_remove.png")