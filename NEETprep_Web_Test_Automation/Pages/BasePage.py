import logging
from playwright.sync_api import Page, Locator, Error as PlaywrightError
from Utilities.LogUtil import Logger
from Utilities import configReader

log = Logger(__name__, logging.INFO)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def _build_locator(self, locator) -> Locator:
        """Turn a conf.ini key (with its _XPATH/_ID/_CSS/_NAME/_LINKTEXT suffix) into a Playwright Locator."""
        # configparser lower-cases keys, so normalise before the lookup
        locator_key = locator.lower()

        try:
            locator_value = configReader.readConfig("locators", locator_key)
        except Exception as e:
            log.logger.error(f"Could not find key '{locator_key}' in config file.")
            raise e

        suffix = locator.upper()
        if suffix.endswith("_XPATH"):
            return self.page.locator(f"xpath={locator_value}")
        if suffix.endswith("_ID"):
            return self.page.locator(f'[id="{locator_value}"]')
        if suffix.endswith("_CSS"):
            return self.page.locator(f"css={locator_value}")
        if suffix.endswith("_NAME"):
            return self.page.locator(f'[name="{locator_value}"]')
        if suffix.endswith("_LINKTEXT"):
            return self.page.get_by_role("link", name=locator_value, exact=True)

        log.logger.error(f"Invalid locator suffix for: {locator}")
        raise ValueError(f"Invalid locator suffix for: {locator}")

    def get_element(self, locator) -> Locator:
        """Return the element's Locator once it is visible (uses the central default timeout)."""
        element = self._build_locator(locator)
        try:
            element.first.wait_for(state="visible")
            return element.first
        except PlaywrightError:
            log.logger.error(f"FAIL: Element '{locator}' not visible")
            raise

    def type(self, locator, value):
        log.logger.info(f"Step: Typing '{value}' into -> {locator}")
        # fill() clears the field before typing
        self.get_element(locator).fill(str(value))

    def click(self, locator):
        log.logger.info(f"Step: Clicking on Element -> {locator}")
        element = self.get_element(locator)
        try:
            # Playwright waits for the element to be visible, enabled and stable
            element.click()
        except PlaywrightError:
            # Same fallback as before: if a normal click fails, force it with JS
            log.logger.info(f"Normal click failed for {locator}, attempting JS click.")
            element.evaluate("el => el.click()")

    def scroll_to_bottom(self):
        """Uses JavaScript to scroll to the bottom of the page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_into_view(self, locator_key):
        """Scrolls until the specific element is in view."""
        self._build_locator(locator_key).first.scroll_into_view_if_needed()

    def is_element_displayed(self, locator):
        """
        Check if an element is visible on the page.
        Returns True if visible, False otherwise.
        """
        try:
            return self.get_element(locator).is_visible()
        except Exception:
            # If element is not found or not visible, return False instead of crashing
            log.logger.error(f"Element {locator} is not displayed on the page.")
            return False
