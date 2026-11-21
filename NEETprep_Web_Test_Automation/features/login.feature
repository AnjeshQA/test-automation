# Login via OTP on www.neetprep.com
# Steps are implemented in TestCases/test_login_bdd.py (step text must match exactly)
# Test data: Excel/testdata.xlsx
#     UserDetail  -> valid mobile number + correct OTP
#     InvalidCred -> valid mobile number + wrong OTP
#
# Tags (run a subset with -m):
#     pytest -m login                 -> every login scenario
#     pytest -m "login and sanity"    -> quick health check (valid login only)
#     pytest -m negative              -> negative tests only

@login
Feature: NEETprep Login Functionality
  As a NEET aspirant
  I want to log in to NEETprep with my mobile number and an OTP
  So that I can reach my dashboard and log out safely

  Background:
    Given the user is on the NEETprep login page

  @sanity @regression
  Scenario: Successful login via OTP
    When the user logs in with valid credentials
    Then the user should be redirected to the home page

  @regression
  Scenario: Successful logout after login
    Given the user is logged in with valid credentials
    When the user logs out
    Then the user should be logged out

  @regression @negative
  Scenario: Login fails with an invalid OTP
    When the user logs in with an invalid OTP
    Then the "Invalid OTP" error message should be displayed
