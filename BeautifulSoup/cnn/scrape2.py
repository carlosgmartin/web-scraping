import csv
import requests
from bs4 import BeautifulSoup

url = 'http://money.cnn.com/data/hotstocks/index.html'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)

most_actives = soup.find('div', attrs={'id': 'wsod_hotStocks'})

table = most_actives.find('table',
                          attrs={'class':
                                 'wsod_dataTable wsod_dataTableBigAlt'})

base_url = 'http://money.cnn.com/'
row_list = []
for row in table.findAll('tr'):
    cell_list = []
    for cell in row.findAll('th'):
        text = cell.text.encode('raw-unicode-escape')
        cell_list.append(text)
    for cell in row.findAll('td'):
        text = cell.text.encode('raw-unicode-escape')
        cell_list.append(text)
    if row.find('a') is not None:
        company_url = base_url + row.find('a').get('href')
        company_response = requests.get(company_url)
        company_html = company_response.content
        company_soup = BeautifulSoup(company_html)
        competitors = company_soup.find('table',
                                        attrs={'class':
                                               'wsod_dataTable ' +
                                               'wsod_dataTableBig ' +
                                               'wsod_quoteCompetitorsModule'})
        for competitor in competitors.findAll('a'):
            cell_list.append(competitor.nextSibling.text)
    row_list.append(cell_list)

outfile = open("./hotstocks.csv", "wb")
writer = csv.writer(outfile)
writer.writerows(row_list)
