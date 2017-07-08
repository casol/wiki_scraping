# Extracting first paragraph from ship URL
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re


def get_details(page_url):
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

def get_image():
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
                print('https://commons.wikimedia.org'+link.attrs['href'])
    except AttributeError:
        print('No Image There')


get_image()


"""
By Rhvanwinkle (Own work) [CC BY-SA 3.0 (http://creativecommons.org/licenses/by-sa/3.0)], via Wikimedia Commons
By Rhvanwinkle (Own work) [<a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY-SA 3.0</a>], <a href="https://commons.wikimedia.org/wiki/File%3AAustralia_(schooner).jpg">via Wikimedia Commons</a>
By USN [Public domain], <a href="https://commons.wikimedia.org/wiki/File%3AAlabama-iii.jpg">via Wikimedia Commons</a>
By USN [Public domain], via Wikimedia Commons
"""