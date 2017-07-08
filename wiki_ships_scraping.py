# Extracting first paragraph from ship URL
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# open URL
html = urlopen('https://en.wikipedia.org/wiki/Akishio_(SS-579)')
# crate BeautifulSoup object
bs_obj = BeautifulSoup(html, 'html.parser')
try:
    print(bs_obj.h1.get_text())
    info = bs_obj.find(id='mw-content-text').findAll('p')[0].get_text()
    # find and remove all footnotes and references e.g [3] [A]
    info = re.sub('\[[A-za-z 0-9]*\]', '', info)
    print(info)
except AttributeError:
    print('Something is missing!')
