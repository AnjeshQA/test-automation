import time
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

# Initialize the driver
driver = webdriver.Chrome()
driver.maximize_window()

# Define a wait time for each element
wait_time = 10

# Function to wait and click element
def wait_and_click(xpath, timeout=wait_time):
    try:
        # Wait for the element to be visible and clickable
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        print(f"Clicked on element with XPath: {xpath}")
    except Exception as e:
        print(f"Error clicking on element with XPath: {xpath} - {str(e)}")

# Function to execute the test Onboarding
def execute_test_flow():
    try:
        driver.get("https://dev.neetprep.com/")

        # Initial wait to ensure page loads completely
        time.sleep(5)

        # Select Practice Question Now at HomePage
        wait_and_click("(//a[normalize-space()='Practice Questions now'])[1]")

        # Additional waits and clicks can be added as necessary

    except Exception as e:
        # Capture the exception message and traceback
        error_message = str(e).replace("'", "\\'").replace("\n", "\\n")
        tb = traceback.format_exc().replace("'", "\\'").replace("\n", "\\n")


        # Extract the line number from the traceback
        line_number = tb.split(", ")[1].split(" ")[1]

        # Inject JavaScript to display the failure message on the browser screen
        driver.execute_script(f"""
            var message = document.createElement('div');
            message.innerHTML = '<strong style="background-color: yellow; color: black;">Test execution failed at line {line_number}</strong>: {error_message}';
            message.style.position = 'fixed';
            message.style.top = '50%';
            message.style.left = '50%';
            message.style.borderRadius = '50px';
            message.style.transform = 'translate(-50%, -50%)';
            message.style.padding = '20px';
            message.style.backgroundColor = '#f44336';
            message.style.color = 'white';
            message.style.fontSize = '20px';
            message.style.zIndex = '1000';
            document.body.appendChild(message);
        """)
        time.sleep(600)
    finally:
        driver.quit()

execute_test_flow()
