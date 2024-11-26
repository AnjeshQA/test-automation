import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to fetch password from PW.rtf file on Desktop
def get_password_from_file():
    try:
        # Path to the PW.rtf file on the Desktop
        file_path = "/Users/ssd/Desktop/PW.rtf"
        with open(file_path, "r") as file:
            password = file.read().strip()  # Read and strip any extra whitespace
        return password
    except FileNotFoundError:
        raise Exception(f"Password file not found at {file_path}. Please ensure it exists.")
    except Exception as e:
        raise Exception(f"Error reading password file: {e}")

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open in maximized window

# Initialize ChromeDriver
service = Service("/usr/local/bin/chromedriver")  # Update with the correct ChromeDriver path
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.neetprep.com/login")

    # Enter the mobile number
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "number"))
    ).send_keys("8882113808")

    # Click the OTP button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@id='otp_button']"))
    ).click()

    time.sleep(3)

    # Fetch password from the file
    password = get_password_from_file()

    # Wait for the password field to appear and enter the password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='Password'])[2]"))
    )
    password_field.send_keys(password)

    # Submit the login
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@id='otp_button']"))
    ).click()

    time.sleep(30)

finally:
    driver.quit()
