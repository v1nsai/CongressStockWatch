from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from seleniumrequests import Chrome
import time

# init
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = Chrome(service=service) #webdriver.Chrome(service=service)
url = "https://efdsearch.senate.gov/search/"

# Click the checkbox
driver.get(url)
# time.sleep(1)
driver.find_element(By.ID, 'agree_statement').click()

# Send the request
driver.find_element(By.CSS_SELECTOR, '#filerTypes.form-check-input.senator_filer').click()
driver.find_element(By.ID, 'fromDate').send_keys('01/01/2022')
response = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary').click()

# Parse results
table = driver.find_element(By.CSS_SELECTOR, '#filedReports_processing.dataTables_processing')
headers = []
theader = table.find_element(By.TAG_NAME, 'theader')
tr = theader.find_elements(By.TAG_NAME, 'tr')
for header in header_row:
    headers.append(header.get_attribute('innerHTML'))


driver.quit()
