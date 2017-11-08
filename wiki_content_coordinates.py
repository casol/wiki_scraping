# Scraping list of museum ships with URLs
from bs4 import BeautifulSoup
from urllib.request import urlopen

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
                wiki_url = link.attrs['href']

                if wiki_url.startswith('/wiki/') or wiki_url.startswith('/w/'):
                    wiki_url = wiki_url.replace('/wiki/', '')
                    wiki_url = wiki_url.replace('/w/', '')
                else:
                    pass
                urls.append(wiki_url)
                # print(link.attrs['href'])
    except AttributeError as e:
        # without title row
        pass

# ships without url
urls.insert(35, 'https://en.wikipedia.org/wiki/Auld_Reekie')
urls.insert(78, 'https://en.wikipedia.org/wiki/Brocklebank')
urls.insert(83, 'https://en.wikipedia.org/wiki/Calshot_Spit_(LV78)')
urls.insert(97, 'https://en.wikipedia.org/wiki/CG_41410')
urls.insert(125, 'https://en.wikipedia.org/wiki/Daniel_Adamson')
urls.insert(129, 'https://en.wikipedia.org/wiki/De_Meern_1')
urls.insert(130, 'https://en.wikipedia.org/wiki/De Wadden')
urls.insert(160, 'https://en.wikipedia.org/wiki/HMS_Expunger_(XE8)')
urls.insert(234, 'https://en.wikipedia.org/wiki/Jacinta')
urls.insert(270, 'https://en.wikipedia.org/wiki/Kranich_P6083')
urls.insert(323, 'https://en.wikipedia.org/wiki/May_Queen')
urls.insert(354, 'https://en.wikipedia.org/wiki/Niederösterreich_(A604)')
urls.insert(467, 'https://en.wikipedia.org/wiki/Spartan')
urls.insert(475, 'https://en.wikipedia.org/wiki/HMS_Stickleback_(X51)')
urls.insert(494, 'https://en.wikipedia.org/wiki/Thalis_o_Milisios')
urls.insert(514, 'https://en.wikipedia.org/wiki/U-461')
urls.insert(530, 'https://en.wikipedia.org/wiki/VIC_56')
urls.insert(539, 'https://en.wikipedia.org/wiki/Weilheim_M1077')
urls.insert(554, 'https://en.wikipedia.org/wiki/PLAN_Xiamen_515')

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

# add wiki url and empty slug field
ii = 0
for ship in new_list:
    ship.append(urls[ii])
    ship.append('')
    ii += 1


wiki_content_api = 'https://en.wikipedia.org//w/api.php?action=query&format=json' \
                   '&prop=extracts&redirects=1&explaintext=1&exsectionformat=plain&titles='
wiki_coordinates_api = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=coordinates&redirects=1&coprop=country&titles='


def ship_content_scraping(content_api):
    """Returns json file with content from each ship in table."""
    ships_content = []
    for ship_url in new_list:
        content_url_api = content_api + ship_url[9]
        try:
            content = urlopen(content_url_api).read().decode('utf-8')
            response_json = json.loads(content)
        except:
            pass
        try:
            # find wikipedia page_id
            page_id = response_json['query']['pages'].keys()
            for key in page_id:
                page_key = key
        except KeyError:
            pass

        try:
            # remove content from Wikipedia article after one of this section
            separators = ['See also', 'References', 'Citations', 'Notes',
                          'Gallery', 'External links', 'Further reading', 'Image gallery']
            # get article
            content_article = response_json['query']['pages'][page_key]['extract']
            sep_id = []
            try:
                for separator in separators:
                    # The find() method returns the lowest index of the substring (if found). If not,  it returns -1
                    s = content_article.find(separator)
                    # check if separator exist in article
                    if s != -1:
                        # create list of existing separators with index e.g. [[174, 'See Also'], [666, 'Notes']]
                        sep_id.append([s, separator])
                # find lowest index of the substring - first appearing in article e.g. [1, 'See Also']
                separator_cut = min(sep_id)
                # Split article and save
                content_article_cut = content_article.split(separator_cut[1], 1)[0]
                ships_content.append(content_article_cut)
            except:
                # probably not best way to handle exception but if something happen just add empty string and move on
                ships_content.append(content_article)

        except KeyError as e:
            # if article does not exist
            content_article = ''
            ships_content.append(content_article)

    ship_id = 1
    database_content = []
    # loop through each article and create dictionary
    for ship_content in ships_content:
        ship_details = {"model": "core.shipdetails", "pk": ship_id,
                        "fields": {"ship": ship_id,
                                   "content": ship_content,
                                   "remarks": ''}}
        database_content.append(ship_details)
        ship_id += 1
    # create json file
    with open('data-content-full-formatted.json', 'w') as f:
        json.dump(database_content, f, ensure_ascii=False)


def ship_coordinates_scrap(coordinates_api):
    """Returns json file with ship museum coordinates."""
    ships_coorinates = []
    for ship_row in new_list:
        content_url_api = coordinates_api + ship_row[9]
        try:
            coordinates = urlopen(content_url_api).read().decode('utf-8')
            response_json = json.loads(coordinates)
        except:
            pass

        try:
            # find wikipedia page_id
            page_id = response_json['query']['pages'].keys()
            for key in page_id:
                page_key = key
        except KeyError:
            pass

        try:
            coordinates_article = response_json['query']['pages'][page_key]['coordinates']
            ships_coorinates.append([coordinates_article[0]['lat'], coordinates_article[0]['lon'], ship_row[1]])
        except:
            # without coordinates
            ships_coorinates.append([None, None, ship_row[1]])

    ship_id = 1
    database_content = []
    # loop through each article and create dictionary
    for ship_location in ships_coorinates:
        ship_coordinate = {"model": "core.shipcoordinates",
                           "pk": ship_id,
                           "fields": {
                               "ship": ship_id,
                               "latitude": ship_location[0],
                               "longitude": ship_location[1],
                               "country": ship_location[2]
                               }
                           }
        database_content.append(ship_coordinate)
        ship_id += 1

    # create json file
    with open('data-coordinates.json', 'w') as f:
        json.dump(database_content, f, ensure_ascii=False)



# run
ship_coordinates_scrap(wiki_coordinates_api)
#ship_content_scraping(wiki_content_api)
