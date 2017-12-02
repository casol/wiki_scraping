# Extracting first paragraph from ship URL
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import os
import re
import json

# Get all ships museums with Wikipedia url
# open url
html = urlopen("https://en.wikipedia.org/w/index.php?title=List_of_museum_ships&diff=808407826&oldid=808133770")
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
urls.insert(130, 'https://en.wikipedia.org/wiki/De_Wadden')
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

x = 1
for url in urls:
    print(x, url)
    x += 1


def get_image_link():
    """Find wiki commons image URL."""
    for ship_url in urls:
        # check if link starts with https
        if ship_url.startswith('https'):
            try:
                html_ship = ship_url
            except:
                pass
        else:
            try:
                html_ship = urlopen('https://en.wikipedia.org/wiki/' + ship_url)
            except:
                pass
        try:
            ship_bs_obj = BeautifulSoup(html_ship, 'html.parser')
        except:
            pass
        try:
            info_table = ship_bs_obj.findAll('table', {'class': 'infobox'})[0]
            info_td = info_table.find('td')
            for img_link in info_td.findAll("a", href=re.compile("^(/wiki/)")):
                if 'href' in img_link.attrs:
                    # e.g. File:Abegweit_in_chicago.jpg
                    return img_link.attrs['href']
        except:
            # no image, move on
            pass


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
    try:
        detail.append(response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['DateTimeOriginal']['value'])
    except KeyError:
        pass
    try:
        # remove hyperlinks from text
        image_description = response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['ImageDescription']['value']
        soup_description = BeautifulSoup(image_description, 'html.parser')
        # find only text in tags
        image_description_formatted = soup_description.findAll(text=True)
        # return list of formatted text
        # join text from list
        text = ''.join(image_description_formatted)
        detail.append(text)
    except:
        pass
    try:
        # remove hyperlinks from text
        artist_details = response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['Artist']['value']
        soup = BeautifulSoup(artist_details, 'html.parser')
        # find only text in tags
        artist_details_formatted = soup.findAll(text=True)
        # return list of formatted text
        # join text from list
        text = ''.join(artist_details_formatted)
        detail.append(text)
    except:
        pass
    try:
        detail.append(response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['UsageTerms']['value'])
    except:
        pass
    try:
        detail.append(response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['LicenseShortName']['value'])
    except:
        pass
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
        # save to
        my_path = '/home/christopher/Desktop/wiki_scraping/wiki_images'
        full_file_name = os.path.join(my_path, image_title)
        urlretrieve(image_location, full_file_name)
    except AttributeError:
        return None

# run

#url = get_image_link()
#print(url)

#get_image(get_image_link())

#print(get_image_detail(get_image_link()))
'''
ship_coordinate = {"model": "core.core.shipimage",
                   "pk": ship_id,
                   "fields": {
                       "ship": ship_id,
                       "image": ship_location[0],
                       "title": ship_location[1],
                       "image_description": ship_location[2],
                       "artist": ship_location[1],
                       "created": ship_location[1],
                       "source_url": ship_location[1],
                       "slug": ship_location[1],
                       "usage_terms": ship_location[1],
                        "license_url": ship_location[1],
                       "license_short_name": ship_location[1]}}
'''
