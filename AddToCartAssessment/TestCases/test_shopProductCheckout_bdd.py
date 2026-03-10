import pytest
from pytest_bdd import scenarios, given, when, then
from Pages.shopProductCheckoutPage import shopProductCheckout
from Utilities import configReader

scenarios('../features/shopProductCheckout.feature')


@given('I am on the shop.NEETprep homepage')
def verify_page_load(driver):
    shop_url = configReader.readConfig("common info", "shop_url")
    driver.get(shop_url)
    # Give the Shop's dynamic header 2 seconds to stabilize
    assert "shop.neetprep.com" in driver.current_url


@when('I search for "HYTS HOME TEST SERIES LATEST EDITION" NEETprep product')
def search_product_step(driver):
    # Fetch product name from [common info] in conf.ini
    product = configReader.readConfig("common info", "product_name")

    shop = shopProductCheckout(driver)
    shop.search_product(product)


@when('I select the product from the search results')
def select_product_step(driver):
    shop = shopProductCheckout(driver)
    shop.select_product()


@when('I click on "Add to Cart" Button')
def click_add_to_cart_step(driver):
    shop = shopProductCheckout(driver)
    shop.click_add_to_cart()


@then('the product should be added to the cart successfully')
def verify_cart_step(driver):
    shop = shopProductCheckout(driver)
    shop.verify_checkout_page()