#TODO make a serie avec les attributs nécesaires (fuck l'objet)
# cmprendre pourquoi certaine request fail
# automatiser
# faire une liste de url à rechercher

import requests
import re
from time import time
from bs4 import BeautifulSoup
from PageParser import parse_from_search_items
import pandas as pd
from datetime import date

website = 'https://www.kijiji.ca'
url = 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/c37l1700281?ad=offering'
numberOfRentals = 0
total = 0

lst_df = list()
i = 0
while(True):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')

    i += 1

    # items = [item.getText().strip() for item in soup.find_all("div", {"class", "price"})]
    # prices = [int(re.sub("[^0-9]", "", item)) / 100 for item in items if item != "Sur demande" and item != "Échange"]
    # fair_prices = [price for price in prices if 5000 > price > 0]
    # total += sum(fair_prices)
    # numberOfRentals += len(fair_prices)
    # print(numberOfRentals)

    items = soup.find_all("div", {"class", "search-item"})

    temp_df = parse_from_search_items(items)

    lst_df.append(temp_df)
    print('nb of rental: ' + str(temp_df.shape[0]))
    print('average price: ' + str(temp_df['price'].mean()))

    if(i>4):
        break

    try:
        url = website + soup.find(title="Suivante").get('href')
    except:
        break


df = pd.concat(lst_df)

date_str = str(date.today())

df.to_pickle('ads_' + date_str + '.pkl')

df = pd.read_pickle('ads_' + date_str + '.pkl')

df = df.loc[df['price'] <= 5000, :]

avgListingPrice = df['price'].mean()
print(avgListingPrice)


