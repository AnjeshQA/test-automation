import pytest
import allure
from Utilities import configReader

# Browser, headed/headless, screenshots and traces come from pytest-playwright CLI options:
#   --browser chromium|firefox|webkit   --headed   --screenshot / --tracing (defaults set in pytest.ini)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Large desktop viewport so the desktop header (and search icon) is visible
    return {**browser_context_args, "viewport": {"width": 1920, "height": 1080}}


@pytest.fixture
def page(page):
    """pytest-playwright's page with the framework's central timeouts applied (see [playwright] in conf.ini)."""
    page.set_default_timeout(float(configReader.readConfig("playwright", "default_timeout_ms")))
    page.set_default_navigation_timeout(float(configReader.readConfig("playwright", "navigation_timeout_ms")))
    return page


@pytest.fixture
def setup(request, page):
    """Used by BaseTest: exposes the Playwright page to class-based tests as self.page."""
    if request.cls is not None:
        request.cls.page = page
    yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)  # Set to autouse so it always monitors
def log_on_failure(request, page):
    """
    Captures screenshots on failure and attaches them to the Allure report.
    """
    yield
    item = request.node
    if hasattr(item, "rep_call") and item.rep_call.failed:
        allure.attach(page.screenshot(full_page=True),
                      name="failure_screenshot",
                      attachment_type=allure.attachment_type.PNG)
