from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import csv


html = urlopen("https://en.wikipedia.org/wiki/List_of_museum_ships")
bs_obj = BeautifulSoup(html, "html.parser")

table = bs_obj.findAll("table", {"class": "wikitable"})[0]

"""
urls = []
for tr in table.findAll('tr'):
    td = tr.find('td')
    urls.append(td)
"""
links = [tr.find('td') for tr in table.findAll('tr')]


"""
rows = []
# easy solution best solution ?
for row in table.findAll("tr"):
    for cell in row.findAll("td"):
        for link in cell.findAll("a", href=re.compile("^(/wiki/)")):
            print(link)
            #if 'href' in link.attrs[0]:
                #print(link.attrs['href'])

        #print(cell)

#print(rows[1])
    #for link in t.findAll("a", href=re.compile("^(/wiki/)")):
        #if 'href' in link.attrs:
            #print(link.attrs['href'])
"""

"""

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
"""