"""
dailyDppScreen - Page Object for the Daily DPP (Daily Practice Problems) screen.

Reached from:
    HomePage.gotoDailyDpp()

Status:
    Only used by TestCases/test_neetprep_end2end.py, which is currently skipped.
    The locators below ('dailyDpp_StartTest_XPATH', 'selectCorrectOptionBy_ID',
    'next_question_XPATH') are NOT in conf.ini yet - add them before enabling that test.
"""
from Pages.BasePage import BasePage

class dailyDppScreen(BasePage):
    def __init__(self, page):
        # Pass the Playwright page up to BasePage (stored as self.page)
        super().__init__(page)

    def dailyDpp(self):
        #start test and go to question page
        self.click("dailyDpp_StartTest_XPATH")
        #seelct correct options from question page
        self.click("selectCorrectOptionBy_ID")
        #go to the next question page
        self.click("next_question_XPATH")
