Feature: NEETprep Login Functionality

  Scenario: Successful login via OTP
    Given the user is on the NEETprep login page
    When the user logs in with valid credentials
    Then the user should be redirected to the home page