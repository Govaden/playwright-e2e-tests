from playwright.sync_api import Locator, Page

class CheckoutPage:

    URL_STEP_ONE = "https://www.saucedemo.com/checkout-step-one.html"
    URL_STEP_TWO = "https://www.saucedemo.com/checkout-step-two.html"
    URL_COMPLETE = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page

    # Locators

    @property
    def first_name_input(self) -> Locator:
        return self.page.locator("#first-name")
    
    @property
    def last_name_input(self) -> Locator:
        return self.page.locator("#last-name")
    
    @property
    def postal_code_input(self) -> Locator:
        return self.page.locator("#postal-code")
    
    @property
    def checkout_button(self) -> Locator:
        return self.page.get_by_role("button", name="Checkout")
    
    @property
    def continue_button(self) -> Locator:
        return self.page.get_by_role("button", name="Continue")
    
    @property
    def finish_button(self) -> Locator:
        return self.page.get_by_role("button", name="Finish")
    
    @property
    def summary_total(self) -> Locator:
        return self.page.locator(".summary_total_label")
    
    @property
    def confirmation_message(self) -> Locator:
        return self.page.locator("xpath=//h2[@class='complete-header']")

    @property
    def error_message(self) -> Locator:
        return self.page.locator('[data-test="error"]')

    def get_overview_item(self, product_name: str) -> Locator:
        """Return a locator matching the overview item by its name."""
        return self.page.locator(".cart_item").filter(has_text=product_name)
    
    # Actions

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def go_to_checkout(self) -> None:
        self.checkout_button.click()

    def continue_checkout(self) -> None:
        self.continue_button.click()

    def finish_checkout(self) -> None:
        self.finish_button.click()