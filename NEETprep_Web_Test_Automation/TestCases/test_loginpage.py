"""
Class-based (non-BDD) login tests, data-driven from Excel/testdata.xlsx.

    test_valid_login   -> sheet "UserDetail":  login with the correct OTP, then log out
    test_invalid_login -> sheet "InvalidCred": login with a wrong OTP, expect "Invalid OTP" error

Each Excel row becomes one test run (@pytest.mark.parametrize).
Inherits BaseTest -> self.page, failure screenshots, one automatic re-run.

Run:
    pytest TestCases/test_loginpage.py
"""
import pytest
from Pages.HomePage import HomePage
from Pages.dailyDppPage import dailyDppScreen
from Pages.loginPage import LoginPage
from TestCases.BaseTest import BaseTest
from Utilities import configReader, dataProvider


class Test_LoginPage(BaseTest):

    # autouse -> runs before every test in this class
    @pytest.fixture(autouse=True)
    def open_site(self, setup):
        # The Selenium version never opened the site before logging in
        self.page.goto(configReader.readConfig("common info", "url"), wait_until="domcontentloaded")

    # One test run per data row in the "UserDetail" sheet (columns: mobileNumber, otp)
    @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("UserDetail"))
    def test_valid_login(self, mobileNumber, otp):
        login = LoginPage(self.page)
        # CHANGED: gotoLoggedIn -> login_with_otp
        # login_with_otp returns HomePage, so we can chain the logout step
        login.login_with_otp(mobileNumber, otp).gotoLogout()

    # One test run per data row in the "InvalidCred" sheet (valid mobile + wrong OTP)
    @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("InvalidCred"))
    def test_invalid_login(self, mobileNumber, otp):
        login = LoginPage(self.page)
        # CHANGED: gotoLoggedIn -> login_with_invalid_otp
        # Asserts that the "Invalid OTP" error message is shown
        login.login_with_invalid_otp(mobileNumber, otp)



    # @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("UserDetail"))
    # def test_loginPage(self, mobileNumber, otp):
    #     login = loginScreen(self.page)
    #     login.gotoLoggedIn(mobileNumber, otp).gotoDailyDpp()
