"""
NOT MEANT FOR PRODUCTION

I'm just trying to figure out how to access the pertinent elements from the parsed html (beautifulsoup object)
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import numpy as np
import pandas as pd

url = "https://www.kijiji.ca/v-appartement-condo/ville-de-montreal/soyez-au-coeur-des-evenements-montrealais-super-studio-luxueux/1550238430"

website = 'https://www.kijiji.ca'
url = 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/c37l1700281?ad=offering'
numberOfRentals = 0
total = 0


response = requests.get(url)
soup = BeautifulSoup(response.content, 'html5lib')
items = [item.getText().strip() for item in soup.find_all("div", {"class", "price"})]

# Find all appartments on one page
items2 = soup.find_all("div", {"class", "search-item"})

item = items2[0]

lst_attributes_div = ['price', 'location']

# Elements of item that are important

"""
"""


def extract_info_from_search_item(item):

    se_values = pd.Series(dtype=object)

    se_values['id'] = item['data-listing-id']
    se_values['url'] = item['data-vip-url']

    se_values['current_date'] = datetime.now()


    price = item.find("div", {"class", "price"})
    location = item.find("div", {"class", "location"})
    title = item.find("div", {"class", "title"})
    description = item.find("div", {"class", "description"})
    nearest_intersection = item.find("span", {"class", "nearest-intersection"})
    bedrooms = item.find("span", {"class", "bedrooms"})
    date_posted = item.find("span", {"class", "date-posted"})

    # Information from elements

    price_text = price.getText().strip()

    if "Sur demande" in price_text:
        price_value = np.nan
        isExchange = False
    elif "Échange" in price_text:
        price_value = np.nan
        isExchange = True

    else:
        price_value = int(re.sub("[^0-9]", "", price_text)) / 100
        isExchange = False

    # Get information from price and is it's an exchange
    se_values['price'] = price_value
    se_values['isExchange'] = isExchange

    # Information simple to get
    se_values['location'] = location.span.getText().strip()
    se_values['title'] = title.getText().strip()
    se_values['description'] = description.getText().strip()
    se_values['date_posted'] = date_posted.getText().strip()

    se_values['nearest_intersection_1'] = nearest_intersection.find_all('span')[0].getText()
    se_values['nearest_intersection_2'] = nearest_intersection.find_all('span')[1].getText()

    bedrooms_pattern = re.compile('(Pièces:)')
    bedrooms_str = bedrooms.getText().strip()

    se_values['nb_bedrooms'] = re.sub(pattern=bedrooms_pattern, repl='', string=bedrooms_str).strip()

    return se_values
