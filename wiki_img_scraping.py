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


def get_image_link():
    """Find wiki commons image URL."""
    wiki_commons_img = []
    ship_id = 0
    for ship_url in urls:
        ship_id += 1
        # check if link starts with https
        if ship_url.startswith('https'):
            try:
                html_ship = urlopen(ship_url)
            except:
                pass
        else:
            try:
                # e.g. HMAS_Advance_(P_83)
                html_ship = urlopen('https://en.wikipedia.org/wiki/' + ship_url)
            except:
                pass
        try:
            ship_bs_obj = BeautifulSoup(html_ship, 'html.parser')
        except:
            pass
        try:
            # find infobox with image
            info_table = ship_bs_obj.findAll('table', {'class': 'infobox'})[0]
            info_td = info_table.find('td')
            for img_link in info_td.findAll("a", href=re.compile("^(/wiki/)")):
                if 'href' in img_link.attrs:
                    # e.g. File:Abegweit_in_chicago.jpg
                    if img_link.attrs['href'].startswith('/wiki/File:'):
                        # e.g. [2, '/wiki/File:Abegweit_in_chicago.jpg']
                        wiki_commons_img.append([ship_id, img_link.attrs['href']])
        except:
            # no image, move on
            pass
    # return list of wiki commons URLS
    return wiki_commons_img


def get_image_detail(wiki_commons_img):
    """Find image detail such as usage terms, artist, image description,
    date, license details."""
    database_img_content = []
    for ship in wiki_commons_img:
        # e.g. /wiki/File:Abegweit_in_chicago.jpg
        link_path = ship[1].replace('/wiki/', '')
        try:
            # retrieve data from Wikipedia API
            response = urlopen('https://en.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop='
                               'extmetadata&titles='+link_path+'&format=json').read().decode('utf-8')
        except HTTPError:
            return print('Page does not exist')
        response_json = json.loads(response)
        # parsing JSON
        try:
            date_time_original = response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['DateTimeOriginal']['value']
        except KeyError:
            date_time_original = ''
        try:
            # remove hyperlinks from text
            image_description = response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['ImageDescription']['value']
            soup_description = BeautifulSoup(image_description, 'html.parser')
            # find only text in tags
            image_description_formatted = soup_description.findAll(text=True)
            # return list of formatted text
            # join text from list
            text = ''.join(image_description_formatted)
            image_description = text
        except:
            image_description = ''
        try:
            # remove hyperlinks from text
            artist_details = response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['Artist']['value']
            soup = BeautifulSoup(artist_details, 'html.parser')
            # find only text in tags
            artist_details_formatted = soup.findAll(text=True)
            # return list of formatted text
            # join text from list
            text = ''.join(artist_details_formatted)
            artist_details = text
        except:
            artist_details = ''
        try:
            usage_terms = response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['UsageTerms']['value']
        except:
            usage_terms = ''
        try:
            license_short_name = response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['LicenseShortName']['value']
        except:
            license_short_name = ''
        try:
            license_url = response_json['query']['pages']['-1']['imageinfo'][0]["extmetadata"]['LicenseUrl']['value']
        except KeyError:
            license_url = ''
        try:
            # format title
            title = response_json['query']['pages']['-1']['title']
            title = title.replace('File:', '')
            title = title.replace('.jpg', '')
        except:
            title = ''
        # create data for model
        ship_img_details = {"model": "core.shipimage",
                            "pk": ship[0],
                            "fields": {
                               "ship": ship[0],
                               "image": link_path.replace('File:', 'images/'),
                               "title": title,
                               "image_description": image_description,
                               "artist": artist_details,
                               "created": date_time_original,
                               "source_url": 'https://commons.wikimedia.org'+ship[1],
                               "usage_terms": usage_terms,
                               "license_url": license_url,
                               "license_short_name": license_short_name}}
        database_img_content.append(ship_img_details)
    # create json file
    with open('database_img_content.json', 'w') as f:
        json.dump(database_img_content, f, ensure_ascii=False)


def get_image(img_links):
    """Download image."""
    for img_link in img_links:
        try:
            html = urlopen('https://commons.wikimedia.org' + img_link[1])
        except:
            print(img_link)
            pass
        try:
            bs_obj = BeautifulSoup(html, 'html.parser')
        except AttributeError:
            pass
        try:
            image_location = bs_obj.find('div', {'class': 'fullMedia'}).find('a')['href']
            # image_title = bs_obj.find('div', {'class': 'fullMedia'}).find('a')['title']
            image_title = img_link[1].replace('/wiki/File:', '')
            # save to
            my_path = '/home/christopher/Desktop/wiki_scraping/wiki_images'
            full_file_name = os.path.join(my_path, image_title)
            urlretrieve(image_location, full_file_name)
        except AttributeError:
            pass

# run
img_links = get_image_link()

get_image(img_links)

get_image_detail(img_links)
