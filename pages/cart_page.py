import allure
from playwright.sync_api import Locator, Page

class CartPage:

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page

    # Locators

    @property
    def cart_badge(self) -> Locator:
        return self.page.locator(".shopping_cart_badge")
    
    # Actions

    def get_product_item(self, product_name: str) -> Locator:
        """Return a locator matching the cart item by its name."""
        return self.page.locator(".inventory_item_name").filter(has_text=product_name)
    
    @allure.step("Remove {product_name} from cart")
    def remove_item(self, product_name: str) -> None:
        """Click the Remove button for the given product in the cart."""
        self.page.locator(".cart_item").filter(
            has_text=product_name
        ).get_by_role("button", name="Remove").click()