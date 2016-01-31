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

for row in table.findAll('tr'):
    for cell in row.findAll('td'):
        print cell.text