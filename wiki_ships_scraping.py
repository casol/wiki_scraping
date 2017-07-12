# Extracting first paragraph from ship URL
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import json


def get_details(page_url):
    """Print first paragraph and title."""
    try:
        html = urlopen('https://en.wikipedia.org'+page_url)
    except HTTPError:
        return print('Page does not exist')
    try:
        # crate BeautifulSoup object
        bs_obj = BeautifulSoup(html, 'html.parser')
    except AttributeError:
        return None
    try:
        print(bs_obj.h1.get_text())
        # get ship coordinates (class='geo' 30.68178; -88.01448)
        print(bs_obj.find('span', {'class': 'geo-dec'}).get_text())
        info = bs_obj.find(id='mw-content-text').findAll('p')[0].get_text()
        # find and remove all footnotes and references e.g [3] [A]
        info = re.sub('\[[A-za-z 0-9]*\]', '', info)
        print(info)
    except AttributeError:
        print('Something is missing!')

# call
#get_details('/wiki/USS_Alabama_(BB-60)')


def get_image_link():
    """Find image link."""
    try:
        html = urlopen('https://en.wikipedia.org/wiki/MV_Abegweit_(1947)')
    except HTTPError:
        return print('Page does not exist')
    try:
        bs_obj = BeautifulSoup(html, 'html.parser')
    except AttributeError:
        return None
    try:
        table = bs_obj.findAll('table', {'class': 'infobox'})[0]
        td = table.find('td')
        #print(td)
        for link in td.findAll("a", href=re.compile("^(/wiki/)")):
            if 'href' in link.attrs:
                return 'https://commons.wikimedia.org'+link.attrs['href']
    except AttributeError:
        print('No Image There')

url = get_image_link()
print(url)


def get_image_detail():
    try:
        response = urlopen('https://en.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extme'
                           'tadata&titles=File:Coast_Guard_Motor_Lifeboat_CG_36500.jpg&format=json').read().decode('utf-8')
    except HTTPError:
        return print('Page does not exist')
    response_json = json.loads(response)
    detail = list()
    detail.append(response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['DateTimeOriginal']['value'])
    detail.append(response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['ImageDescription']['value'])
    detail.append(response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['Artist']['value'])
    detail.append(response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['UsageTerms']['value'])
    detail.append(response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['LicenseShortName']['value'])
    try:
        detail.append(response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['LicenseUrl']['value'])
    except KeyError:
        pass
    return detail

#print(get_image_detail())


def get_image():
    html = urlopen('https://commons.wikimedia.org/wiki/File:Abegweit_in_chicago.jpg')
    bs_obj = BeautifulSoup(html, 'html.parser')
    image_location = bs_obj.find('a', {'class': 'fullMedia'}).find('href')
    urlretrieve(image_location, 'ship.jpg')

get_image()
