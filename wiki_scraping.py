import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv


html = urlopen("https://en.wikipedia.org/wiki/List_of_museum_ships")
bs_obj = BeautifulSoup(html, "html.parser")

table = bs_obj.findAll("table", {"class": "wikitable"})[0]

# urls
urls = []
for tr in table.findAll('tr'):
    td = tr.find('td')
    try:
        for link in td.findAll("a", href=re.compile("^(/wiki/)|^(/w/)")):
            if 'href' in link.attrs:
                print(link.attrs['href'])
                urls.append(link)
    except AttributeError as e:
        # without title row
        pass


#links = [tr.find('td') for tr in table.findAll('tr')]

# table
rows = table.findAll("tr")
csv_file = open('/home/christopher/Desktop/wiki_scraping/table.csv', 'wt')
writer = csv.writer(csv_file)

try:
    for row in rows:
        csv_row = []
        for cell in row.findAll(['td']):
            csv_row.append(cell.get_text())
            writer.writerow(csv_row)
finally:
    csv_file.close()
