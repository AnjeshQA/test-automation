# Search a product on shop.neetprep.com and add it to the cart (no payment is made)
# Steps are implemented in TestCases/test_shopProductCheckout_bdd.py (step text must match exactly)
# The searched product name comes from conf.ini [common info] product_name

Feature: shop.NEETprep product add to cart Functionality

  Scenario: Search for a product and add it to the cart successfully
    Given I am on the shop.NEETprep homepage
    When I search for "HYTS HOME TEST SERIES LATEST EDITION" NEETprep product
    And I select the product from the search results
    And I click on "Add to Cart" Button
    Then the product should be added to the cart successfully