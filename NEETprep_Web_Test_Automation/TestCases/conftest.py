"""
conftest.py - shared pytest fixtures and hooks for every test in TestCases/.

pytest loads this file automatically; tests never import it.

What it provides:
    browser_type_launch_args -> headed/headless switch from HEADED / SLOWMO in .env
    browser_context_args -> browser window settings (viewport) for every test
    page                 -> the Playwright page every test/step uses (with central timeouts)
    setup                -> gives class-based tests (BaseTest) access to the page as self.page
    valid_user / invalid_user -> login test data from Excel/testdata.xlsx
    logged_in_home_page  -> opens the site, logs in, returns the HomePage (reuse in any test)
    shared BDD steps     -> "the user is on the NEETprep login page"
                            "the user is logged in to the NEETprep platform"
    log_on_failure       -> attaches a screenshot to the Allure report when a test fails

Where the browser comes from:
    The pytest-playwright plugin creates browser -> context -> page for each test and
    closes them afterwards (fresh, independent session per test). Choose it on the CLI:
        --browser chromium|firefox|webkit   --headed   (headless is the default)
    Or set HEADED=1 in a local .env file (see .env.example) to always show the browser.
    Screenshots/traces on failure are configured in pytest.ini (--screenshot / --tracing).
"""
import os

import pytest
import allure
from pytest_bdd import given

from Pages.loginPage import LoginPage
from Utilities import configReader, dataProvider

# Load the local .env file (gitignored) into environment variables, e.g. HEADED=1.
# Values already set in the shell win over .env (HEADED=0 pytest ... forces headless).
# If python-dotenv is not installed, skip it - HEADED can still be set in the shell.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Load the local .env file (gitignored) into environment variables, e.g. HEADED=1.
# Values already set in the shell win over .env (HEADED=0 pytest ... forces headless).
# If python-dotenv is not installed, skip it - HEADED can still be set in the shell.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Browser, headed/headless, screenshots and traces come from pytest-playwright CLI options:
#   --browser chromium|firefox|webkit   --headed   --screenshot / --tracing (defaults set in pytest.ini)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Headed/headless switch. Overrides pytest-playwright's browser launch options.
        HEADED=1  -> show the browser window (SLOWMO=<ms> optionally pauses between actions)
        anything else / not set -> unchanged: headless, unless --headed is passed on the CLI
    CI has no .env, so Jenkins / GitHub Actions always stay headless.
    """
    if os.getenv("HEADED") == "1":
        return {**browser_type_launch_args,
                "headless": False,
                "slow_mo": float(os.getenv("SLOWMO", "0"))}
    return browser_type_launch_args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Extends pytest-playwright's default context settings (one per test session).
    # Large desktop viewport so the desktop header (and search icon) is visible
    return {**browser_context_args, "viewport": {"width": 1920, "height": 1080}}


@pytest.fixture
def page(page):
    """pytest-playwright's page with the framework's central timeouts applied (see [playwright] in conf.ini)."""
    # Max wait for element actions/waits (click, fill, wait_for ...)
    page.set_default_timeout(float(configReader.readConfig("playwright", "default_timeout_ms")))
    # Max wait for page.goto() and other navigations
    page.set_default_navigation_timeout(float(configReader.readConfig("playwright", "navigation_timeout_ms")))
    return page


@pytest.fixture
def setup(request, page):
    """Used by BaseTest: exposes the Playwright page to class-based tests as self.page."""
    # request.cls is the test class (None for plain function tests such as the BDD steps)
    if request.cls is not None:
        request.cls.page = page
    # Hand the page to the test; pytest-playwright closes it after the test
    yield page


# =============================================================================
# Shared login: test data, login fixture and shared BDD steps
#
# Write the login once here and reuse it in every test that needs a logged-in user
# (download PDF, custom practice, Daily DPP ...), instead of repeating the login steps.
#
#   BDD feature file  -> use the shared step text:
#       Background:
#         Given the user is logged in to the NEETprep platform
#     The step returns the HomePage, so later steps can take `home_page` as an argument.
#
#   Plain pytest test -> ask for the fixture:
#       def test_something(logged_in_home_page): ...
#
# pytest-bdd steps defined in conftest.py are available to every test_*_bdd.py file.
# =============================================================================
def _first_row(sheet_name):
    """Return (mobile, otp) from the first data row of an Excel sheet, or fail with a clear message."""
    data = dataProvider.get_data(sheet_name)
    if not data:
        pytest.fail(f"Excel sheet '{sheet_name}' is empty or could not be read!")
    # Column A = mobile number, column B = OTP
    return data[0][0], data[0][1]


@pytest.fixture
def valid_user():
    """Valid mobile number + correct OTP (Excel sheet UserDetail)."""
    return _first_row("UserDetail")


@pytest.fixture
def invalid_user():
    """Valid mobile number + wrong OTP (Excel sheet InvalidCred)."""
    return _first_row("InvalidCred")


@pytest.fixture
def logged_in_home_page(page, valid_user):
    """
    Opens the site, logs in with the valid test account and returns the HomePage (dashboard).
    Fails in setup (before the test body runs) if the dashboard does not load.
    """
    mobile, otp = valid_user
    home = LoginPage(page).open().login_with_otp(mobile, otp)
    assert home.is_dashboard_visible(), "Login precondition failed: dashboard not shown!"
    return home


@given('the user is on the NEETprep login page', target_fixture="login_page")
def open_login_page(page):
    """Shared step: open the landing page. Later steps get it as the `login_page` argument."""
    login = LoginPage(page).open()
    assert "neetprep.com" in page.url, f"Expected a neetprep.com URL, got {page.url}"
    return login


@given('the user is logged in to the NEETprep platform', target_fixture="home_page")
def user_is_logged_in(logged_in_home_page):
    """Shared step: logged-in user on the dashboard. Later steps get it as `home_page`."""
    return logged_in_home_page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Runs after each test phase (setup / call / teardown).
    # Stores the result on the test item (item.rep_setup, item.rep_call, ...)
    # so fixtures like log_on_failure can see whether the test failed.
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)  # Set to autouse so it always monitors
def log_on_failure(request, page):
    """
    Captures screenshots on failure and attaches them to the Allure report.
    """
    # Everything before yield runs before the test, everything after runs after it
    yield
    item = request.node
    # Only attach a screenshot if the test body ("call" phase) failed
    if hasattr(item, "rep_call") and item.rep_call.failed:
        allure.attach(page.screenshot(full_page=True),
                      name="failure_screenshot",
                      attachment_type=allure.attachment_type.PNG)
