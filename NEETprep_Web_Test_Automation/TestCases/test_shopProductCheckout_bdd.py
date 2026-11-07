import pytest
from pytest_bdd import scenarios, given, when, then
from Pages.shopProductCheckoutPage import shopProductCheckout
from Utilities import configReader

scenarios('../features/shopProductCheckout.feature')


@given('I am on the shop.NEETprep homepage')
def verify_page_load(page):
    shop_url = configReader.readConfig("common info", "shop_url")
    # The old time.sleep(2) is gone: later actions auto-wait for the dynamic header
    page.goto(shop_url, wait_until="domcontentloaded")
    assert "shop.neetprep.com" in page.url


@when('I search for "HYTS HOME TEST SERIES LATEST EDITION" NEETprep product')
def search_product_step(page):
    # Fetch product name from [common info] in conf.ini
    product = configReader.readConfig("common info", "product_name")

    shop = shopProductCheckout(page)
    shop.search_product(product)


@when('I select the product from the search results')
def select_product_step(page):
    shop = shopProductCheckout(page)
    shop.select_product()


@when('I click on "Add to Cart" Button')
def click_add_to_cart_step(page):
    shop = shopProductCheckout(page)
    shop.click_add_to_cart()


@then('the product should be added to the cart successfully')
def verify_cart_step(page):
    shop = shopProductCheckout(page)
    shop.verify_checkout_page()
