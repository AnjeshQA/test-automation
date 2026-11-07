"""
shopProductCheckout - Page Object for the NEETprep shop (https://shop.neetprep.com).

Used by:
    TestCases/test_shopProductCheckout_bdd.py
    (features/shopProductCheckout.feature - search a product and add it to the cart)

Flow:
    search icon -> type product name -> pick search result -> Add to Cart
    -> Check out -> verify the "Pay now" button (no payment is made)
"""
from Pages.BasePage import BasePage

class shopProductCheckout(BasePage):
    def __init__(self, page):
        # Pass the Playwright page up to BasePage (stored as self.page)
        super().__init__(page)

    def search_product(self, product_name):
        # Open the search modal from the header search icon
        self.click("shop_click_searchBox_CSS")
        # Ensure your BasePage type method takes (locator_key, value)
        # Type the product name (comes from conf.ini [common info] product_name)
        self.type("shop_inputSearchBox_XPATH", product_name)

    def select_product(self):
        # Open the first predictive-search result (the HYTS product)
        self.click("click_HYTS_SearchResults_XPATH")

    def click_add_to_cart(self):
        # Add the product to the cart from the product page
        self.click("shop_addToCart_XPATH")

    def verify_checkout_page(self):
        # Go from the cart drawer to the checkout page
        self.click("shop_checkout_XPATH")
        # We scroll first to ensure the button is in the DOM/View
        self.scroll_into_view("payNowButton_XPATH")
        # Now we check if it's actually there (we never click it - no real payment)
        assert self.is_element_displayed("payNowButton_XPATH"), "Checkout failed: Pay Now button not visible!"
