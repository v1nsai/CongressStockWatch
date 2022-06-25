from bs4 import BeautifulSoup
import cloudscraper

senate_stock_disclosures_url = 'https://sec.report/Senate-Stock-Disclosures/'

def get_current_disclosures():
    # Grab and parse main page
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

# with open('test_scrape.json', 'w') as file:
#     output_string = json.dumps(output).replace('},', '},\n')
#     file.write(output_string)