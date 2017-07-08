# Scraping list of museum ships with URLs
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

# open url
html = urlopen("https://en.wikipedia.org/wiki/List_of_museum_ships")
# create BeautifulSoup object
bs_obj = BeautifulSoup(html, "html.parser")
# find wikitable
table = bs_obj.findAll("table", {"class": "wikitable"})[0]

# urls
urls = []
for tr in table.findAll('tr'):
    # select all first <td> inside all <tr>
    td = tr.find('td')
    try:
        # find all URLs starting with /wiki/ or /w/
        for link in td.findAll("a", href=re.compile("^(/wiki/)|^(/w/)")):
            if 'href' in link.attrs:  # returns a Python dictionary object
                # add to the list
                urls.append('https://en.wikipedia.org' + link.attrs['href'])
                #print(link.attrs['href'], urls.index(link))
    except AttributeError as e:
        # without title row
        pass

urls.insert(23, 'ANGARA')
for url in urls:
    print(url)


"""
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
"""