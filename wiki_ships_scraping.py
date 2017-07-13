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


def get_image_link():
    """Find wiki commons image URL."""
    try:
        html = urlopen('https://en.wikipedia.org/wiki/SS_X-1')
    except HTTPError:
        return print('Page does not exist')
    try:
        bs_obj = BeautifulSoup(html, 'html.parser')
    except AttributeError:
        return None
    try:
        table = bs_obj.findAll('table', {'class': 'infobox'})[0]
        td = table.find('td')
        for link in td.findAll("a", href=re.compile("^(/wiki/)")):
            if 'href' in link.attrs:
                # e.g. File:Abegweit_in_chicago.jpg
                return link.attrs['href']
    except AttributeError:
        print('No Image There')


def get_image_detail(link_path):
    """Find image detail such as usage terms, artist, image description,
    date, license details."""
    link_path = link_path.replace('/wiki/', '')
    try:
        response = urlopen('https://en.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop='
                           'extmetadata&titles='+link_path+'&format=json').read().decode('utf-8')
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


def get_image(link_path):
    """Download image."""
    try:
        html = urlopen('https://commons.wikimedia.org' + link_path)
    except HTTPError:
        return print('Page does not exist')
    try:
        bs_obj = BeautifulSoup(html, 'html.parser')
    except AttributeError:
        return None
    try:
        image_location = bs_obj.find('div', {'class': 'fullMedia'}).find('a')['href']
        # maybe not original size? something small like a preview image
        image_title = bs_obj.find('div', {'class': 'fullMedia'}).find('a')['title']
        # print(image_location, image_title)
        urlretrieve(image_location, image_title)
    except AttributeError:
        return None

# run

url = get_image_link()
print(url)

get_image(get_image_link())

print(get_image_detail(get_image_link()))
