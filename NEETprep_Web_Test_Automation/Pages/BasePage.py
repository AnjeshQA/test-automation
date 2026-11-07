"""
BasePage - the parent class of every Page Object.

Purpose:
    Holds the shared, low-level browser actions (find, click, type, scroll, visibility check)
    so the individual Page Objects only describe *business steps* (e.g. "login with OTP").

How it is used:
    class LoginPage(BasePage): ...
    LoginPage(page).click("login_sendOTP_button_XPATH")

    Every action takes a *locator key* from ConfigurationData/conf.ini [locators] instead of a
    raw selector. The key's suffix (_XPATH, _ID, _CSS, _NAME, _LINKTEXT) tells this class how
    to build the Playwright locator.

Next step after this file:
    See Pages/loginPage.py for an example Page Object built on top of these methods.
"""
import logging

# Page    -> the browser tab object given to us by the pytest-playwright `page` fixture
# Locator -> Playwright's lazy "element finder"; it re-queries the DOM on every action
# Error   -> base class of all Playwright errors (TimeoutError is a subclass of it)
from playwright.sync_api import Page, Locator, Error as PlaywrightError

# Framework helpers: file logger and the conf.ini reader
from Utilities.LogUtil import Logger
from Utilities import configReader

# File logger for this module -> writes to Logs/log<date>.txt
log = Logger(__name__, logging.INFO)


class BasePage:
    def __init__(self, page: Page):
        # Store the Playwright page so every child Page Object can use self.page
        self.page = page

    def _build_locator(self, locator) -> Locator:
        """Turn a conf.ini key (with its _XPATH/_ID/_CSS/_NAME/_LINKTEXT suffix) into a Playwright Locator."""
        # configparser lower-cases keys, so normalise before the lookup
        locator_key = locator.lower()

        # Read the selector text for this key from conf.ini [locators]
        try:
            locator_value = configReader.readConfig("locators", locator_key)
        except Exception as e:
            # The key is missing in conf.ini -> log it clearly and fail the test
            log.logger.error(f"Could not find key '{locator_key}' in config file.")
            raise e

        # Pick the Playwright selector type from the key's suffix
        suffix = locator.upper()
        if suffix.endswith("_XPATH"):
            # XPath selector, e.g. //button[@id='otp_button']
            return self.page.locator(f"xpath={locator_value}")
        if suffix.endswith("_ID"):
            # Element id; attribute form also works for ids with special characters
            return self.page.locator(f'[id="{locator_value}"]')
        if suffix.endswith("_CSS"):
            # CSS selector, e.g. body > div > span
            return self.page.locator(f"css={locator_value}")
        if suffix.endswith("_NAME"):
            # name="..." attribute (form fields)
            return self.page.locator(f'[name="{locator_value}"]')
        if suffix.endswith("_LINKTEXT"):
            # Exact visible text of a link (<a>), like Selenium's By.LINK_TEXT
            return self.page.get_by_role("link", name=locator_value, exact=True)

        # Unknown suffix -> configuration mistake, stop the test with a clear message
        log.logger.error(f"Invalid locator suffix for: {locator}")
        raise ValueError(f"Invalid locator suffix for: {locator}")

    def get_element(self, locator) -> Locator:
        """Return the element's Locator once it is visible (uses the central default timeout)."""
        element = self._build_locator(locator)
        try:
            # .first = first match (same as Selenium's find_element);
            # wait_for waits up to default_timeout_ms (conf.ini) for it to be visible
            element.first.wait_for(state="visible")
            return element.first
        except PlaywrightError:
            # Not visible in time -> log and re-raise so the test fails with Playwright's call log
            log.logger.error(f"FAIL: Element '{locator}' not visible")
            raise

    def type(self, locator, value):
        log.logger.info(f"Step: Typing '{value}' into -> {locator}")
        # fill() clears the field before typing; str() because Excel data may be numbers
        self.get_element(locator).fill(str(value))

    def click(self, locator):
        log.logger.info(f"Step: Clicking on Element -> {locator}")
        element = self.get_element(locator)
        try:
            # Playwright waits for the element to be visible, enabled and stable
            element.click()
        except PlaywrightError:
            # Same fallback as before: if a normal click fails, force it with JS
            # (e.g. the element is covered by an overlay)
            log.logger.info(f"Normal click failed for {locator}, attempting JS click.")
            element.evaluate("el => el.click()")

    def scroll_to_bottom(self):
        """Uses JavaScript to scroll to the bottom of the page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_into_view(self, locator_key):
        """Scrolls until the specific element is in view."""
        # Playwright also scrolls automatically before click/fill; this is for explicit scrolling
        self._build_locator(locator_key).first.scroll_into_view_if_needed()

    def is_element_displayed(self, locator):
        """
        Check if an element is visible on the page.
        Returns True if visible, False otherwise.
        """
        try:
            # get_element waits for visibility first, so slow pages still return True
            return self.get_element(locator).is_visible()
        except Exception:
            # If element is not found or not visible, return False instead of crashing
            log.logger.error(f"Element {locator} is not displayed on the page.")
            return False
