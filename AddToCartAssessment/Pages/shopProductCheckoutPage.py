from Pages.BasePage import BasePage

class shopProductCheckout(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def search_product(self, product_name):
        self.click("shop_click_searchBox_CSS")
        # Ensure your BasePage type method takes (locator_key, value)
        self.type("shop_inputSearchBox_XPATH", product_name)

    def select_product(self):
        self.click("click_HYTS_SearchResults_XPATH")

    def click_add_to_cart(self):
        self.click("shop_addToCart_XPATH")

    def verify_checkout_page(self):
        self.click("shop_checkout_XPATH")
        # We scroll first to ensure the button is in the DOM/View
        self.scroll_into_view("payNowButton_XPATH")
        # Now we check if it's actually there
        assert self.is_element_displayed("payNowButton_XPATH"), "Checkout failed: Pay Now button not visible!"