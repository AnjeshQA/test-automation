import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://dev.neetprep.com/")

driver.find_element(By.LINK_TEXT, "Login/Register").click()
#driver.find_element(By.ID,"email").send_keys("apptesting@goodeducator.com")
driver.find_element(By.ID, "number").send_keys("8882113808")
#driver.find_element(By.XPATH,"(//button[normalize-space()='Sign in with Google'])[1]").click()
driver.find_element(By.XPATH, "//a[@id='otp_button']").click()
time.sleep(3)
driver.find_element(By.XPATH, "(//input[@placeholder='Password'])[2]").send_keys("")
driver.find_element(By.XPATH, "//a[@id='otp_button']").click()

time.sleep(2)
