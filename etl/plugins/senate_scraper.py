import pandas as pd

from sys import path
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

error_timeout = 30
count = 1

def wait_for_element(driver, by, selector):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, selector)))  

def scrape_current_page(driver):
    '''Scrape the next page into a pd.DataFrame'''

    table_inner_html = driver.find_element(By.ID, 'filedReports').get_attribute('innerHTML').replace('\n', '')
    table_html = f'<table>{table_inner_html}</table>'
    df = pd.read_html(table_html)[0]
    
    # write_to_schema(df)

    # global count
    # df.to_csv(f'scraped_pages/page_{count}.csv', index=False)
    # count += 1
    return df
    
def scrape_all():
    # init
    options = FirefoxOptions()
    options.headless = True
    # driver_location = 'driver/geckodriver'
    driver_location = '/opt/airflow/selenium/driver/geckodriver'
    service = FirefoxService(executable_path=driver_location)
    path.append(driver_location)
    driver = webdriver.Firefox(options=options, service=service)
    url = "https://efdsearch.senate.gov/search/"
    sleep_duration = 1

    # Click the checkbox
    driver.get(url)
    wait_for_element(driver, By.ID, 'agree_statement').click()

    # Send the request
    wait_for_element(driver, By.CSS_SELECTOR, '#filerTypes.form-check-input.senator_filer').click()
    wait_for_element(driver, By.ID, 'fromDate').send_keys('01/01/2022')
    wait_for_element(driver, By.CSS_SELECTOR, '.btn.btn-primary').click()

    # Parse results on first page to dataframe
    try:
        print('Processing page 1')
        sleep(sleep_duration)
        records = scrape_current_page(driver)
    except NoSuchElementException:
        print('Failed to get first page')

    # Append other pages to dataframe
    while True:
        try:
            # Go to next page
            last_page = wait_for_element(driver, By.CSS_SELECTOR, f'a.paginate_button.current')
            last_page_num = int(last_page.text)
            current_page = wait_for_element(last_page, By.XPATH, f'..')
            current_page = wait_for_element(current_page, By.LINK_TEXT, f'{last_page_num + 1}')
            current_page.click()
            sleep(sleep_duration)

            # Scrape current page
            current_page_num = int(wait_for_element(driver, By.CSS_SELECTOR, f'a.paginate_button.current').text)
            print(f'Processing page {current_page_num}')
            df = scrape_current_page(driver)
            records = pd.concat([records, df], ignore_index=True)
        except TimeoutException:
            print(f'Failed to find page {last_page_num + 1}, likely because the process has reached the last page')
            break

    driver.quit()
    return records.to_csv()

# scrape_all()