import time
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from NEETprep.NEETprep_Login import driver

# Define a wait time for each element
wait_time = 10

# Function to wait and click element
def wait_and_click(xpath, timeout=wait_time):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)  # Scroll to element
        element.click()
    except Exception as e:
        driver.save_screenshot("error_screenshot.png")  # Save screenshot on failure
        raise e

# Function to execute the test flow
def execute_test_flow():
    try:
        # Initial wait
        time.sleep(2)

        # Navigate to the target page directly
        driver.get("https://www.neetprep.com/newui/subjectSelection")

        # Verify the page is loaded
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='customPracticeBtn']"))
        )

        # Select Practice Session--Custom Practice Session
        wait_and_click("//a[@id='customPracticeBtn']")

        # Click "Custom Practice" option
        wait_and_click("//div[@class='flex-grow overflow-auto px-4']//button[1]")

        # Proceed
        wait_and_click("//div[@class='p-4 w-full absolute bottom-0']")

        # Choose chapter & topic
        wait_and_click("(//input[@type='checkbox'])[1]")

        # Click Continue
        wait_and_click("//button[normalize-space()='Continue']")

        # Additional interactions
        wait_and_click("(//div[@class='cursor-pointer flex items-center justify-between gap-4 w-full'])[1]")
        wait_and_click("//input[@id='Easy']")
        wait_and_click("//button[normalize-space()='Okay']")
        wait_and_click("//p[normalize-space()='Include Bookmarked']")
        wait_and_click("(//*[name()='path'])[6]")
        wait_and_click("//p[normalize-space()='Include Incorrect']")
        wait_and_click("(//*[name()='path'])[6]")
        wait_and_click("(//div[@class='cursor-pointer flex items-center justify-between gap-4 w-full'])[2]")
        wait_and_click("//button[normalize-space()='Continue']")

        # Inject JavaScript to display success message
        driver.execute_script("""
            var message = document.createElement('div');
            message.innerHTML = "Congratulations! Test flow completed successfully.";
            message.style.position = 'fixed';
            message.style.top = '20px';
            message.style.left = '20px';
            message.style.borderRadius = '50px';
            message.style.padding = '20px';
            message.style.backgroundColor = '#4CAF50';
            message.style.color = 'white';
            message.style.fontSize = '20px';
            message.style.fontWeight = '600';
            message.style.zIndex = '1000';
            document.body.appendChild(message);
        """)
        time.sleep(120)

    except Exception as e:
        # Capture the exception message and traceback
        error_message = str(e)
        traceback_str = traceback.format_exc()

        # Log error and save screenshot
        print("Error:", error_message)
        print("Traceback:", traceback_str)
        driver.save_screenshot("error_screenshot.png")

        # Inject failure message into the browser
        driver.execute_script(f"""
            var message = document.createElement('div');
            message.innerHTML = "Test failed: {error_message.replace("'", "\\'")}";
            message.style.position = 'fixed';
            message.style.top = '20px';
            message.style.left = '20px';
            message.style.borderRadius = '50px';
            message.style.padding = '20px';
            message.style.backgroundColor = '#f44336';
            message.style.color = 'white';
            message.style.fontSize = '20px';
            message.style.fontWeight = '600';
            message.style.zIndex = '1000';
            document.body.appendChild(message);
        """)
        time.sleep(120)

# Execute the test flow
execute_test_flow()
