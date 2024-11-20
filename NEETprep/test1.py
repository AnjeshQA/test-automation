import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to securely get password input from the terminal
def get_password():
    return input("Enter your password securely: ")

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open in maximized window

# Initialize ChromeDriver
service = Service("/usr/local/bin/chromedriver")  # Update with the correct ChromeDriver path
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://dev.neetprep.com/")

# Click Login/Register
WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.LINK_TEXT, "Login/Register"))
).click()

# Enter the mobile number
WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.ID, "number"))
).send_keys("8882113808")

# Click the OTP button
WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.XPATH, "//a[@id='otp_button']"))
).click()

time.sleep(3)

# Get password securely from the terminal
password = get_password()

# Wait for the password field to appear and enter the password
password_field = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='Password'])[2]"))
)
password_field.send_keys(password)

# Submit the login
WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.XPATH, "//a[@id='otp_button']"))
).click()

time.sleep(3)
