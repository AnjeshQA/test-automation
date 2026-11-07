import pytest
from pytest_bdd import scenarios, given, when, then

from Utilities import configReader
from Pages.loginPage import LoginPage
from Utilities import dataProvider

scenarios('../features/login.feature')

@given('the user is on the NEETprep login page')
def verify_page_load(page):
    url = configReader.readConfig("common info", "url")

    # Navigate to the site (conftest does not do it)
    page.goto(url, wait_until="domcontentloaded")
    assert "neetprep.com" in page.url


@when('the user logs in with valid credentials')
def login_step(page):
    # CHANGED: 'LoginTest' -> 'UserDetail' to match your Excel file
    data = dataProvider.get_data("UserDetail")

    # Industry Standard: Add a check to ensure Excel isn't empty
    if not data:
        pytest.fail("Excel sheet 'UserDetail' is empty or could not be read!")

    mobile, otp = data[0][0], data[0][1]

    login = LoginPage(page)
    login.login_with_otp(mobile, otp)

@then('the user should be redirected to the home page')
def verify_dashboard(page):
    from Pages.HomePage import HomePage
    home = HomePage(page)
    assert home.is_dashboard_visible(), "User was not redirected to Dashboard!"
