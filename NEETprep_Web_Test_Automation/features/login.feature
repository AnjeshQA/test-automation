# Login via OTP on www.neetprep.com
# Steps are implemented in TestCases/test_login_bdd.py (step text must match exactly)
# Test data (mobile number, OTP): Excel/testdata.xlsx, sheet UserDetail

Feature: NEETprep Login Functionality

  Scenario: Successful login via OTP
    Given the user is on the NEETprep login page
    When the user logs in with valid credentials
    Then the user should be redirected to the home page