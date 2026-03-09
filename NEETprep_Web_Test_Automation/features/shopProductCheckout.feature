Feature: shop.NEETprep product add to cart Functionality

  Scenario: Search for a product and add it to the cart successfully
    Given I am on the shop.NEETprep homepage
    When I search for "HYTS HOME TEST SERIES LATEST EDITION" NEETprep product
    And I select the product from the search results
    And I click on "Add to Cart" Button
    Then the product should be added to the cart successfully