from selenium import webdriver
from time import sleep

driver = webdriver.Chrome()
driver.get('https://my.e-klase.lv/Family/ReportPupilMarks/Get')
sleep(1)
driver.

driver.get_screenshot_as_file("screenshot.png")
driver.quit()
