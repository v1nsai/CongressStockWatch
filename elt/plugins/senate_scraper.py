from bs4 import BeautifulSoup
import cloudscraper
import requests
import json

# def get_current_disclosures():
# Get all new disclosures for today's date

# Retrieve the CSRF token and define constants
session = requests.Session()
url = 'https://efdsearch.senate.gov/search/'
r = session.get(url)
csrf_token = session.cookies.get('csrftoken')    
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Referer": f'{url}'
}
body = f"prohibition_agreement=1&first_name=&last_name=&filer_type=1&senator_state=&submitted_start_date=&submitted_end_date=&csrfmiddlewaretoken={csrf_token}"

# Grab results
response = session.post(url, body, headers)
print()


# with open('test_scrape.json', 'w') as file:
#     output_string = json.dumps(output).replace('},', '},\n')
#     file.write(output_string)















def get_current_disclosures():
    # Grab and parse main page
    senate_stock_disclosures_url = 'https://sec.report/Senate-Stock-Disclosures/'

    scraper = cloudscraper.create_scraper()
    raw_text = scraper.get(senate_stock_disclosures_url).text
    soup = BeautifulSoup(raw_text, features='lxml')

    # Find the table and break it into rows
    tbody = soup.select("#document_heading tbody")[0]

    count = 1
    output = []
    for tr in tbody.find_all('tr'):
        # Each row is actually 2 rows for some stupid reason, so grouping them with mod
        if count % 2 == 1:
            td = tr.find('td')
            file_date = td.find('div', {"style": "float:left"}).text
            transaction_date = td.find('div', {"style": "float:right"}).text
            td = td.findNext('td')
            issuer = td.a.text
            td = td.findNext('td')
            reporter = td.div.text.replace('\n', '')
        if count % 2 == 0:
            td = tr.find('td')
            type = td.text.split(' ')
            if len(type) == 2:
                transaction_type = type[0]
                transaction_hash = type[1]
            if len(type) == 3:
                transaction_type = f'{type[0]} {type[1]}'
                transaction_hash = type[2]
            td = td.findNext('td')
            amount = td.text
            td = td.findNext('td')
            ownership = td.find('div', {"style": "float:right;"}).text
            row = {
                "file_date": file_date,
                "transaction_date": transaction_date,
                "issuer": issuer,
                "reporter": reporter,
                "transaction_type": transaction_type,
                "transaction_hash": transaction_hash,
                "amount": amount,
                "ownership": ownership
            }
            output.append(row)
        count = count + 1
    
    return output