import time
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from NEETprep.NEETprep_Login import driver

# Define a wait time for each element
wait_time = 2

# Function to wait and click element
def wait_and_click(xpath, timeout=wait_time):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

# Function to execute the test flow
def execute_test_flow():
    try:
        # Initial wait
        time.sleep(2)

        # Select Practice Session--Custom Practice Session
        wait_and_click("//a[@id='customPracticeBtn']")
        # Click "Custom Practice" option https://dev.neetprep.com/newui/subjectSelection
        wait_and_click("//div[@class='flex-grow overflow-auto px-4']//button[1]")

        # Click to proceed
        wait_and_click("//div[@class='p-4 w-full absolute bottom-0']")

        # Choose chapter & topic
        wait_and_click("(//input[@type='checkbox'])[1]")

        # Click Continue
        wait_and_click("//button[normalize-space()='Continue']")

        # Select chapter and difficulty
        wait_and_click("(//div[@class='cursor-pointer flex items-center justify-between gap-4 w-full'])[1]")

        # Select difficulty level
        wait_and_click("//input[@id='Easy']")

        # Click Okay
        wait_and_click("//button[normalize-space()='Okay']")

        # Include bookmarked
        wait_and_click("//p[normalize-space()='Include Bookmarked']")
        wait_and_click("(//*[name()='path'])[6]")

        # Include incorrect
        wait_and_click("//p[normalize-space()='Include Incorrect']")
        wait_and_click("(//*[name()='path'])[6]")

        # Select second chapter
        wait_and_click("(//div[@class='cursor-pointer flex items-center justify-between gap-4 w-full'])[2]")

        # Click Continue
        wait_and_click("//button[normalize-space()= 'Continue']")

        # Final wait for the page to load
        time.sleep(2)

        # Inject JavaScript to display the success message on the browser screen
        driver.execute_script("""
            var message = document.createElement('div');
            message.innerHTML = "Congratulations! The test flow for the 'Question Selection' trial user has been completed";
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
        error_message = str(e).replace("'", "\\'").replace("\n", "\\n")
        tb = traceback.format_exc().replace("'", "\\'").replace("\n", "\\n")

        # Extract the line number from the traceback safely
        try:
            line_number = tb.split(", ")[1].split(" ")[1]
        except IndexError:
            line_number = "Unknown"

        # Inject JavaScript to display the failure message on the browser screen with a "Close" button
        driver.execute_script(f"""
            var message = document.createElement('div');
            message.innerHTML = '<strong style="background-color: yellow; color: black;">Test execution failed at line {line_number}</strong>: {error_message}<br><br><button id="closeButton" style="padding:10px; background-color:black; color:white; border:none; border-radius:5px; cursor:pointer;">Close</button>';
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
            
            // Add an event listener to the "Close" button
            document.getElementById('closeButton').addEventListener('click', function() {{
                message.style.display = 'none'; // Hide the message when the button is clicked
        }});
        """)

        time.sleep(600)

# Execute the test flow
execute_test_flow()
