import allure
from playwright.sync_api import Page, expect
import pytest
from pages.cart_page import CartPage
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
def test_cart(logged_in_page: Page, products_to_add, product_to_remove):
    page = logged_in_page
    inventory = InventoryPage(page)
    cart = CartPage(page)

    expect(page).to_have_url(InventoryPage.URL_PATTERN)
    expect(inventory.inventory_list).to_be_visible()

    for product_name in products_to_add:
        inventory.add_product_to_cart(product_name)

    expect(cart.cart_badge).to_have_text(str(len(products_to_add)))

    inventory.open_cart()
    expect(page).to_have_url(CartPage.URL_PATTERN)
    
    for product_name in products_to_add:
        expect(cart.get_product_item(product_name)).to_be_visible()

    cart.remove_item(product_to_remove)

    expect(cart.get_product_item(product_to_remove)).not_to_be_visible()
    expect(cart.cart_badge).to_have_text(str(len(products_to_add) - 1))

    for product_name in products_to_add:
        if product_name != product_to_remove:
            expect(cart.get_product_item(product_name)).to_be_visible()

    page.screenshot(path="test_results/test_cart/screenshot_cart_remove.png")