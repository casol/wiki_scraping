# Scraping list of museum ships with URLs
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import json
import re
import unicodedata


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
        for link in td.findAll("a", href=re.compile("^(/wiki/)|^(/w/)|^(https)")):
            if 'href' in link.attrs:  # returns a Python dictionary object
                # add to the list
                urls.append(link.attrs['href'])
                #print(link.attrs['href'], urls.index(link))
    except AttributeError as e:
        # without title row
        pass


for url in urls:
    print(url)

# links = [tr.find('td') for tr in table.findAll('tr')]

# table
rows = table.findAll("tr")

ships = []
for row in rows:
    for cell in row.findAll(['td']):
        ship = cell.get_text()
        # Return the normal form form for the Unicode string unistr (xa0)
        ship = unicodedata.normalize('NFKD', ship)
        ship = re.sub('\[[A-za-z 0-9]*\]', '', ship)
        ship = re.sub('\\n', '', ship)
        ships.append(ship)

# from list of cells in table create lists of ships
# e.g. ['BAE Abdón Calderón', 'Ecuador', 'Guayas', 'Guayaquil', 'Ecuador', '1884', '', 'Naval ship', '']
new_list = [ships[i:i+9] for i in range(0, len(ships), 9)]

#for ship_list in new_list:
    #print(ship_list)


"""
taki model powinien byc
d = {"model": "core.shiplist",
      "pk": 1,
      "fields": {"ship": "USS Albacore",
                 "country": "United States",
                 "region": "New Hampshire",
                 "city": "Portsmouth",
                 "from_country": "United States",
                 "year": "1953",
                 "ship_class": "Teardrop hull",
                 "ship_type": "Submarine",
                 "remarks":"National Register of Historic Places",
                 "url":"https://en.wikipedia.org/wiki/USS_Albacore_(AGSS-569)",
                 "slug":"uss-albacore"}
                 }

print(d['fields']['ship'])
"""