import pandas as pd
import logging

from sys import path
from time import sleep
# from xvfbwrapper import Xvfb

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

error_timeout = 30
count = 1

def scrape_current_page(driver):
    '''Scrape the next page into a pd.DataFrame'''

    table_inner_html = driver.find_element(By.ID, 'filedReports').get_attribute('innerHTML').replace('\n', '')
    table_html = f'<table>{table_inner_html}</table>'
    logging.info(f'table_html = {table_html}')
    df = pd.read_html(table_html)[0]
    global count
    # df.to_csv(f'scraped_pages/page_{count}.csv', index=False)
    count += 1
    return df
    
def scrape_all():
    # init
    options = FirefoxOptions()
    options.headless = True
    driver_location = 'elt/driver/geckodriver'
    service = FirefoxService(executable_path=driver_location)
    path.append('./elt/driver/')
    driver = webdriver.Firefox(options=options, service=service)
    url = "https://efdsearch.senate.gov/search/"
    sleep_duration = 3

    # Click the checkbox
    driver.get(url)
    driver.find_element(By.ID, 'agree_statement').click()

    # Send the request
    driver.find_element(By.CSS_SELECTOR, '#filerTypes.form-check-input.senator_filer').click()
    driver.find_element(By.ID, 'fromDate').send_keys('01/01/2022')
    driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary').click()

    # Parse results on first page to dataframe
    try:
        sleep(sleep_duration)
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
            sleep(sleep_duration)
            df = scrape_current_page(driver)
            records = pd.concat([records, df], ignore_index=True)
        except NoSuchElementException:
            print(f'Failed to find page {last_page_num + 1}, likely because the process has reached the last page')
            break

    # vdisplay.stop()
    driver.quit()
    records.to_csv('records.csv', index=None)
    # return records

scrape_all()