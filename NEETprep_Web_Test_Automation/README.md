# NEETprep Web Test Automation

Automated UI tests for **www.neetprep.com** and **shop.neetprep.com**.

**Stack:** Python · Playwright · Pytest · pytest-bdd (Gherkin) · Page Object Model · Allure / pytest-html · Jenkins

> Migrated from Selenium to Playwright in Nov 2026. The old Selenium version is kept on the
> `selenium-framework` branch for reference.

---

## 1. How the framework works

```
features/*.feature          What to test, in plain English (Gherkin: Given / When / Then)
        │
TestCases/test_*.py         Step definitions + class-based tests (pytest)
        │
Pages/*.py                  Page Objects: business actions per page (login, search, checkout…)
        │
Pages/BasePage.py           Shared actions: find, click, type, scroll, is-visible
        │
ConfigurationData/conf.ini  Locators (selectors), URLs, timeouts
Excel/testdata.xlsx         Test data (mobile number, OTP)
        │
Playwright                  Drives the real browser (Chromium / Firefox / WebKit)
```

**Example: what happens when the login scenario runs**
1. `features/login.feature` says *"When the user logs in with valid credentials"*.
2. pytest-bdd finds the step with that exact text in `TestCases/test_login_bdd.py`.
3. The step reads the mobile number and OTP from `Excel/testdata.xlsx` (sheet `UserDetail`).
4. It calls `LoginPage(page).login_with_otp(mobile, otp)`.
5. `LoginPage` calls `BasePage.click("login_sendOTP_button_XPATH")` and similar.
6. `BasePage` looks up that key in `conf.ini` and asks Playwright to click it. Playwright waits
   automatically until the element is visible and clickable.

### Why the Page Object Model?
Tests describe **what** to do (log in, add to cart). Page Objects know **how** to do it on the
page. When the website changes, you usually fix **one selector in `conf.ini`** and don't touch
the tests.

### Selenium vs Playwright: what changed for you
| Before (Selenium) | Now (Playwright) |
|---|---|
| `driver` fixture | `page` fixture |
| `WebDriverWait` / `time.sleep` | Not needed. Playwright waits automatically |
| chromedriver + webdriver-manager | `python -m playwright install` |
| Screenshot only | Screenshot **and trace** (step-by-step replay) on failure |

---

## 2. Folder and file guide

| Path | Purpose |
|---|---|
| `features/login.feature` | BDD scenario: log in via OTP |
| `features/shopProductCheckout.feature` | BDD scenario: search a shop product, add to cart, reach checkout |
| `TestCases/conftest.py` | Shared fixtures: `page` (with timeouts), viewport, `setup` for class tests, Allure screenshot on failure |
| `TestCases/BaseTest.py` | Parent class for class-based tests: gives `self.page`, failure screenshot, 1 automatic re-run |
| `TestCases/test_login_bdd.py` | Step definitions for `login.feature` |
| `TestCases/test_shopProductCheckout_bdd.py` | Step definitions for `shopProductCheckout.feature` |
| `TestCases/test_loginpage.py` | Data-driven login tests: valid login + logout, and invalid OTP |
| `TestCases/test_neetprep_end2end.py` | Login → Daily DPP flow. **Skipped**: its locators aren't defined yet |
| `Pages/BasePage.py` | Parent of all Page Objects. Turns `conf.ini` keys into Playwright locators |
| `Pages/loginPage.py` | Landing page and OTP login form |
| `Pages/HomePage.py` | Logged-in dashboard: dashboard check, logout, Daily DPP |
| `Pages/shopProductCheckoutPage.py` | Shop: search, select product, add to cart, checkout check |
| `Pages/dailyDppPage.py` | Daily DPP screen (used only by the skipped end-to-end test) |
| `ConfigurationData/conf.ini` | URLs, product name, Playwright timeouts, **all locators** |
| `Excel/testdata.xlsx` | Test data. `UserDetail` = valid login, `InvalidCred` = valid mobile + wrong OTP |
| `Utilities/configReader.py` | `readConfig(section, key)` reads `conf.ini` |
| `Utilities/dataProvider.py` | `get_data(sheet)` reads Excel rows for `@pytest.mark.parametrize` |
| `Utilities/LogUtil.py` | File logger, writes to `Logs/log<date>.txt` |
| `Utilities/ExcelReader.py` | Old Excel helpers. Not used, and it writes to the Excel file when run |
| `Utilities/scroll_util.py` | Old mobile (Appium) swipe helpers. Not used by web tests |
| `pytest.ini` | pytest settings: Allure output, screenshots/traces on failure, logging, timeout |
| `requirements.txt` | Python dependencies |
| `jenkins_run.sh` | CI script used by Jenkins |

**Generated folders** (git-ignored, recreated on every run):

| Folder | Content |
|---|---|
| `test-results/` | Screenshot and `trace.zip` for each failed test |
| `allure-results/` | Raw data for the Allure report |
| `reports/` | pytest-html report, when run with `--html` |
| `Logs/` | Daily framework log files |

---

## 3. Setup (one time)

Requires **Python 3.10+**. Run these from the `NEETprep_Web_Test_Automation` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install         # downloads Chromium, Firefox, WebKit
```

On Linux, if a browser complains about missing libraries, run: `sudo .venv/bin/playwright install-deps`

**PyCharm:** set the interpreter to `.venv` and the working directory of the run configuration to
`NEETprep_Web_Test_Automation`.

---

## 4. Running tests

Always run from the `NEETprep_Web_Test_Automation` folder.

| Goal | Command |
|---|---|
| Run everything (headless Chromium) | `pytest` |
| Watch the browser | `pytest --headed` |
| Slow down to watch each step | `pytest --headed --slowmo 500` |
| Another browser | `pytest --browser firefox` or `--browser webkit` |
| Several browsers | `pytest --browser chromium --browser firefox` |
| One file | `pytest TestCases/test_login_bdd.py` |
| One test | `pytest -k test_invalid_login` |
| Only collect (no browser) | `pytest --collect-only` |
| HTML report | `pytest --html=reports/report.html --self-contained-html` |
| Pause and debug with Playwright Inspector | `PWDEBUG=1 pytest -k test_valid_login` |

### Reports and debugging failures
- **Trace (best tool):** `playwright show-trace test-results/<test-name>/trace.zip`
  This shows every step with a screenshot, the DOM, console and network.
- **Screenshot:** `test-results/<test-name>/test-failed-1.png`
- **Allure:** `allure serve allure-results` (needs the Allure CLI)
- **HTML:** open `reports/report.html`
- **Logs:** `Logs/log<date>.txt`

### Timeouts
Set once in `conf.ini`:
```ini
[playwright]
default_timeout_ms = 20000      ; max wait for clicks / typing / element visible
navigation_timeout_ms = 30000   ; max wait for page loads
```
`pytest.ini` also sets `timeout = 300`: the hard limit per test, in seconds.

---

## 5. How to add things

### A new locator
Add it to `[locators]` in `conf.ini`. Choose the suffix based on the selector type:
```ini
# Dashboard
myNewButton_XPATH=//button[text()='Start']
searchField_ID=input-search
```
Then use it in a Page Object: `self.click("myNewButton_XPATH")`.
Tip: `playwright codegen https://www.neetprep.com` opens a browser and suggests selectors as you click.

### A new Page Object
```python
# Pages/customPracticePage.py
from Pages.BasePage import BasePage

class CustomPracticePage(BasePage):
    def start_fresh(self):
        self.click("noStartFresh_XPATH")
```

### A new BDD scenario
1. Write the scenario in `features/<name>.feature`.
2. Create `TestCases/test_<name>_bdd.py`:
```python
from pytest_bdd import scenarios, given, when, then
scenarios('../features/<name>.feature')

@given('the user is on the NEETprep login page')
def open_site(page):
    page.goto("https://www.neetprep.com")
```
The step text must match the feature file **exactly**. Steps get the browser through the `page` argument.

### A new class-based, data-driven test
```python
class Test_Something(BaseTest):
    @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("UserDetail"))
    def test_x(self, mobileNumber, otp):
        LoginPage(self.page).login_with_otp(mobileNumber, otp)
```
Remember to open the site first. See the `open_site` fixture in `test_loginpage.py`.

### New test data
Add a row to a sheet in `Excel/testdata.xlsx`. Each row becomes one test run. Don't put real
users' credentials in the repo. Use the test account only.

---

## 6. Jenkins

The Jenkins job's **Execute shell** step:
```bash
cd NEETprep_Web_Test_Automation
chmod +x jenkins_run.sh && ./jenkins_run.sh
```
The script:
1. updates the code
2. creates or activates `.venv`
3. installs `requirements.txt`
4. installs the Playwright browser
5. runs pytest **headless** with Allure and HTML reports

Optional job parameters or environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `GIT_BRANCH_TO_TEST` | `master` | Branch to test |
| `TEST_PATH` | `TestCases/test_loginpage.py` | Tests to run, e.g. `TestCases` for all |
| `BROWSER` | `chromium` | `chromium`, `firefox` or `webkit` |

**Post-build → Archive artifacts:** `allure-results/**, reports/**, test-results/**, Logs/**`
(prefix with `NEETprep_Web_Test_Automation/` if the job runs from the repo root).
On a Linux agent, change the browser install line to `python -m playwright install --with-deps "$BROWSER"`.

---

## 7. Current test status (Nov 2026)

| Test | Status |
|---|---|
| Login BDD: successful login via OTP | ✅ Passing |
| Shop BDD: search and add to cart | ✅ Passing (Chromium, Firefox) |
| `test_valid_login` (login + logout) | ✅ Passing |
| `test_invalid_login` (wrong OTP shows error) | ✅ Passing |
| End-to-end Daily DPP (3 tests) | ⏭ Skipped: needs Daily DPP locators in `conf.ini` |

**Known issues**
- Closing the landing-page popup falls back to a JS click every time, which adds about 20 s per login test.
  A more precise locator for `landingPage_close_classroom_dialogBox_XPATH` would remove that delay.
- `shop_click_searchBox_CSS` is a long position-based CSS path, so it will break if the shop header layout changes.
- Locators break when the website UI changes. Fix them in `conf.ini` (see section 5).

---

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| `Timeout 20000ms exceeded … waiting for locator(...)` | The selector no longer matches a visible element. Open the trace, then update the locator in `conf.ini` |
| `No option '<key>' in section: 'locators'` | The key is missing from `conf.ini`, or misspelled |
| `Executable doesn't exist … ms-playwright` | Run `python -m playwright install` |
| `Host system is missing dependencies` (Linux) | `sudo .venv/bin/playwright install-deps` |
| Tests show `[NOTSET]` | Excel file or sheet not found. Check `Excel/testdata.xlsx` (capital **E**) |
| `ModuleNotFoundError: Pages` / `Utilities` | Run pytest from the `NEETprep_Web_Test_Automation` folder |
| `fixture 'driver' not found` | Old Selenium code. Use `page` (BDD steps) or `self.page` (class tests) |
