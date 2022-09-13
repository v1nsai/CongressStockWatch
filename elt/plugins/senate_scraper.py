import pandas as pd
import logging

from time import sleep
from xvfbwrapper import Xvfb

from selenium import webdriver
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions

error_timeout = 30
count = 1

def scrape_current_page(driver):
    '''Scrape the next page into a pd.DataFrame'''

    table_inner_html = driver.find_element(By.ID, 'filedReports').get_attribute('innerHTML').replace('\n', '')
    table_html = f'<table>{table_inner_html}</table>'
    df = pd.read_html(table_html)[0]
    global count
    df.to_csv(f'scraped_pages/page_{count}.csv', index=False)
    count += 1
    return df
    
def scrape_all():
    # init
    # vdisplay = Xvfb()
    # vdisplay.start()
    # service = Service(executable_path=ChromeDriverManager().install())
    options = FirefoxOptions()
    # options.headless = True
    driver = webdriver.Firefox(options=options)
    # driver = webdriver (executable_path=ChromeDriverManager().install(), options=options)
    url = "https://efdsearch.senate.gov/search/"

    # Click the checkbox
    driver.get(url)
    driver.find_element(By.ID, 'agree_statement').click()

    # Send the request
    driver.find_element(By.CSS_SELECTOR, '#filerTypes.form-check-input.senator_filer').click()
    driver.find_element(By.ID, 'fromDate').send_keys('01/01/2022')
    driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary').click()

    # Parse results on first page to dataframe
    try:
        sleep(2)
        records = scrape_current_page(driver)
    except NoSuchElementException:
        print('Failed to get first page')

    # Append other pages to dataframe
    while True:
        try:
            # Go to next page
            last_page = driver.find_element(By.CSS_SELECTOR, f'a.paginate_button.current')
            last_page_num = int(last_page.text)
            current_page = last_page.find_element(By.XPATH, f'..').find_element(By.LINK_TEXT, f'{last_page_num + 1}')
            current_page.click()
            print(f'Processing page {current_page.text}')
            sleep(1)
            df = scrape_current_page(driver)
            records = pd.concat([records, df], ignore_index=True)
        except NoSuchElementException:
            print(f'Failed to find page {last_page_num + 1}, likely because the process has reached the last page')
            break

    # vdisplay.stop()
    driver.quit()
    return records

scrape_all()
