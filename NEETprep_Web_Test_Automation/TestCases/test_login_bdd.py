"""
BDD step definitions for features/login.feature (pytest-bdd).

Scenarios covered:
    1. Successful login via OTP        -> dashboard is shown          (@sanity @regression)
    2. Successful logout after login   -> Login/Register link is back (@regression)
    3. Login fails with an invalid OTP -> "Invalid OTP" error shown   (@regression @negative)

How it works:
    scenarios(...) turns every Scenario in the feature file into a pytest test.
    Each Given/When/Then line in the feature file is matched (by exact text) to a
    function decorated with the same text, here or in conftest.py.

Shared pieces live in TestCases/conftest.py (reused by every feature):
    Background step "the user is on the NEETprep login page" -> gives `login_page`
    fixtures `valid_user` / `invalid_user`                    -> Excel test data

Conventions used here (common pytest-bdd practice):
    - Background         -> the shared "open the site" step is written once in the feature file
    - Tags -> markers    -> @sanity / @regression / @negative let you run subsets with -m
    - target_fixture     -> a step returns a Page Object and later steps receive it as an argument
    - Asserts in Then    -> Page Objects only return True/False; the Then steps decide pass/fail

Run:
    pytest TestCases/test_login_bdd.py
    pytest TestCases/test_login_bdd.py -m sanity
"""
from pytest_bdd import scenarios, given, when, then

from Pages.HomePage import HomePage

# Generate tests from all scenarios in the feature file (path is relative to this file)
scenarios('../features/login.feature')


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------
@given('the user is logged in with valid credentials', target_fixture="home_page")
def logged_in_user(login_page, valid_user):
    # Precondition for the logout scenario. The Background already opened the site,
    # so log in on that page (other features use the shared
    # "the user is logged in to the NEETprep platform" step from conftest.py instead).
    mobile, otp = valid_user
    home = login_page.login_with_otp(mobile, otp)
    assert home.is_dashboard_visible(), "Precondition failed: user could not log in!"
    return home


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------
@when('the user logs in with valid credentials', target_fixture="home_page")
def login_with_valid_credentials(login_page, valid_user):
    mobile, otp = valid_user
    # login_with_otp returns the HomePage object -> shared as `home_page`
    return login_page.login_with_otp(mobile, otp)


@when('the user logs in with an invalid OTP')
def login_with_invalid_otp(login_page, invalid_user):
    mobile, wrong_otp = invalid_user
    # Same flow as a valid login; the site should reject the OTP and stay on the login form
    login_page.login_with_otp(mobile, wrong_otp)


@when('the user logs out')
def logout(home_page):
    home_page.gotoLogout()


# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------
@then('the user should be redirected to the home page')
def verify_dashboard(home_page: HomePage):
    # Pass = a dashboard-only element is visible
    assert home_page.is_dashboard_visible(), "User was not redirected to Dashboard!"


@then('the user should be logged out')
def verify_logged_out(login_page):
    # Pass = the landing page's Login/Register link is visible again
    assert login_page.is_login_link_visible(), "User is still logged in: Login/Register link not shown!"


@then('the "Invalid OTP" error message should be displayed')
def verify_invalid_otp_error(login_page):
    assert login_page.is_invalid_otp_error_displayed(), "'Invalid OTP' error message was NOT visible!"
