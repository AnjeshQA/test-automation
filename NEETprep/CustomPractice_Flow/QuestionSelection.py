import time
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from NEETprep.NEETprep_Login import driver
from selenium.webdriver.support.ui import Select

# Define a wait time for each element
wait_time = 2

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
        time.sleep(4)

        #wait_and_click("(//a[@id='customPracticeBtn'])[1]")
        driver.find_element(By.XPATH, "(//a[@id='customPracticeBtn'])[1]").click()
        #wait_and_click("(//span[normalize-space()='Custom Practice Session'])[1]")



        #driver.get("https://www.neetprep.com/home")

        # Verify the page is loaded &  # Select Practice Session--Custom Practice Session
        #WebDriverWait(driver, wait_time).until(
        #   EC.presence_of_element_located((By.XPATH, "(//a[@id='customPracticeBtn'])[1]"))
        #).click()


        #select the chapter
        select_Subject = driver.find_element(by=By.XPATH, value="//body//div//button[2]")
        select_Subject.click()

        time.sleep(2)
        #click Next Button

        nextButton = driver.find_element(By.XPATH, "//button[normalize-space()='Next']")
        nextButton.click()

        time.sleep(2)

        #select Chapters Topic
        #driver.find_element(By.XPATH, "(//input[@id='c645'])[1]").click()
        driver.find_element(By.CSS_SELECTOR, "#c645").click()

        time.sleep(2)

        #Chapter level difficulty and filter


        driver.find_element(By.XPATH, "//button[normalize-space()='Continue']").click()

        time.sleep(2)

        driver.find_element(By.XPATH, "//p[normalize-space()='Difficulty Level']").click()

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='Easy']").click()

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='Medium']").click()

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='Hard']").click()

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='Include Bookmarked']").click()

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='Include Incorrect']").click()

        time.sleep(1)

        driver.find_element(By.XPATH, "//button[normalize-space()='Continue']").click()


        time.sleep(2)


        #free trail page-- select question count.

        select_Question_count=driver.find_element(By.XPATH, "//span[normalize-space()='5 questions']")
        select_Question_count.click()
        #driver.find_element(By.CSS_SELECTOR, "button[class='w-full bg-[#E6A123] hover:bg-[#cc9210] transition-colors text-white py-3.5 px-5 rounded-[10px] text-base font-semibold']").click()

        time.sleep(2)

        #Question Option select

        #driver.find_element(By.XPATH, "//div[contains(@class,'flex items-center gap-x-4 mt-5 py-4 px-4')]//button[3]").click()

        time.sleep(1)

        driver.find_element(By.XPATH, "(//*[name()='path'][@id='Vector_3'])[1]").click()

        time.sleep(2)
        #print("Error at Next action")
        time.sleep(2)

        #Next Button to enter Question Page.
        driver.find_element(By.XPATH, "(//button[normalize-space()=\"Let's go\"])[1]").click()


        time.sleep(3)

        repeat_count = 5

        for _ in range(repeat_count):
            wait_and_click("(//button[@id='option-3'])[1]",2)
            wait_and_click("(//*[name()='path'])[13]",2)


        wait_and_click("(//button[normalize-space()='Yes'])[1]",2)
        time.sleep(2)

        wait_and_click("(//button[normalize-space()='Continue'])[1]",2)
        time.sleep(2)

        wait_and_click("(//button[normalize-space()='Continue your journey'])[1]",2)
        time.sleep(2)

        wait_and_click("(//button[normalize-space()='Go Home'])[1]",2)

        time.sleep(60)

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
