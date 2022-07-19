from time import sleep
from numpy import integer

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException

error_timeout = 30

def scrape_current_page():
    '''Scrape the next page into a pd.DataFrame'''

    table_inner_html = driver.find_element(By.CSS_SELECTOR, '#filedReports.table.table-striped.dataTable.no-footer').get_attribute('innerHTML').replace('\n', '')
    table_html = f'<table>{table_inner_html}</table>'
    df = pd.read_html(table_html)[0]
    return df
    
def scrape_all():
    # init
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
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
        sleep(1)
        records = scrape_current_page()
    except NoSuchElementException:
        print('Failed to get first page')

    # Append other pages to dataframe
    while True:
        try:
            # Go to next page
            last_page = driver.find_element(By.CSS_SELECTOR, f'a.paginate_button.current')
            last_page_num = int(last_page.text)
            current_page = last_page.find_element(By.XPATH, f'..').find_element(By.LINK_TEXT, f'{last_page_num}')
            current_page.click()
            print(f'Processing page {current_page.text}')
            if int(current_page.text) == 5:
                pass
            sleep(1)
            df = scrape_current_page()
            records = pd.concat([records, df], ignore_index=True)
        except NoSuchElementException:
            print(f'Failed to find page {current_page.text}, likely because the process has reached the last page')
            break

    records.to_csv('senate_dump_07182022.csv', na_rep='', index=False)
    driver.quit()