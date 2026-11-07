"""
BDD step definitions for features/login.feature (pytest-bdd).

How it works:
    scenarios(...) turns every Scenario in the feature file into a pytest test.
    Each Given/When/Then line in the feature file is matched (by exact text) to the
    function decorated with the same text below. Steps receive the Playwright `page`
    fixture from conftest.py.

Run:
    pytest TestCases/test_login_bdd.py
"""
import pytest
from pytest_bdd import scenarios, given, when, then

from Utilities import configReader
from Pages.loginPage import LoginPage
from Utilities import dataProvider

# Generate tests from all scenarios in the feature file (path is relative to this file)
scenarios('../features/login.feature')

@given('the user is on the NEETprep login page')
def verify_page_load(page):
    # Base URL comes from conf.ini [common info]
    url = configReader.readConfig("common info", "url")

    # Navigate to the site (conftest does not do it)
    # "domcontentloaded" = continue as soon as the HTML is parsed (like Selenium's 'eager')
    page.goto(url, wait_until="domcontentloaded")
    assert "neetprep.com" in page.url


@when('the user logs in with valid credentials')
def login_step(page):
    # CHANGED: 'LoginTest' -> 'UserDetail' to match your Excel file
    # Read login data from Excel/testdata.xlsx, sheet "UserDetail"
    data = dataProvider.get_data("UserDetail")

    # Industry Standard: Add a check to ensure Excel isn't empty
    if not data:
        pytest.fail("Excel sheet 'UserDetail' is empty or could not be read!")

    # First data row: column A = mobile number, column B = OTP
    mobile, otp = data[0][0], data[0][1]

    # Perform the whole login flow through the Page Object
    login = LoginPage(page)
    login.login_with_otp(mobile, otp)

@then('the user should be redirected to the home page')
def verify_dashboard(page):
    from Pages.HomePage import HomePage
    home = HomePage(page)
    # Pass = a dashboard-only element is visible
    assert home.is_dashboard_visible(), "User was not redirected to Dashboard!"
