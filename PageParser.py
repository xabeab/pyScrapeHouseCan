from bs4 import BeautifulSoup
import re
from datetime import datetime
import numpy as np
import pandas as pd
import requests


def parse_from_search_item(item):

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
    is_exchange = False

    if "Sur demande" in price_text:
        price_value = np.nan
    elif "Échange" in price_text:
        price_value = np.nan
        is_exchange = True

    else:
        price_value = int(re.sub("[^0-9]", "", price_text)) / 100

    # Get information from price and is it's an exchange
    se_values['price'] = price_value
    se_values['isExchange'] = is_exchange

    # Information simple to get
    se_values['location'] = location.span.getText().strip()
    se_values['title'] = title.getText().strip()
    se_values['description'] = description.getText().strip()
    se_values['date_posted'] = date_posted.getText().strip()

    if nearest_intersection is None:
        se_values['nearest_intersection_1'] = None
        se_values['nearest_intersection_2'] = None

    else:
        se_values['nearest_intersection_1'] = nearest_intersection.find_all('span')[0].getText()
        se_values['nearest_intersection_2'] = nearest_intersection.find_all('span')[1].getText()

    bedrooms_pattern = re.compile('(Pièces:)')
    bedrooms_str = bedrooms.getText().strip()

    se_values['nb_bedrooms'] = re.sub(pattern=bedrooms_pattern, repl='', string=bedrooms_str).strip()

    return se_values


def parse_from_search_items(items):

    lst_se = list()

    for i in range(len(items)):
        print(i)
        temp_se = parse_from_search_item(items[i])

        lst_se.append(temp_se)

    df = pd.DataFrame(lst_se)

    return df


def parse_kijiji(url: str) -> pd.DataFrame:

    website = 'https://www.kijiji.ca'

    lst_df = list()
    i = 0
    while (True):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')

        i += 1

        items = soup.find_all("div", {"class", "search-item"})

        temp_df = parse_from_search_items(items)

        lst_df.append(temp_df)
        print('nb of rental: ' + str(temp_df.shape[0]))
        print('average price: ' + str(temp_df['price'].mean()))

        if (i > 4):
            break

        try:
            url = website + soup.find(title="Suivante").get('href')
        except:
            break

    df = pd.concat(lst_df)

    now = pd.Timestamp.now()

    df['first_extracted'] = now
    df['last_extracted'] = now

    # df['time_open'] = df['first_extracted'] - df['last_extracted']

    return df




