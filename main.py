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

import pandas_gbq
from SQLOperations import SQLOperations
from TableUpdater import TableUpdater
import pandas as pd
import os

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

now = pd.Timestamp.now()

df['first_extracted'] = now
df['last_extracted'] = now

df['time_open'] = df['first_extracted'] - df['last_extracted']

date_str = str(date.today())

df.to_pickle('ads_' + date_str + '.pkl')

## CREATE FIRST TABLE

sql_ops = SQLOperations()

cols_to_compare = ['price', 'title', 'date_posted', 'nb_bedrooms',  'nearest_intersection_1', 'nearest_intersection_2', 'nb_bedrooms']

##### temp first table
# df = df.drop_duplicates(subset=cols_to_compare)
# pandas_gbq.to_gbq(df, 'adds.adds_detail', project_id=sql_ops.project_id, if_exists='replace')
#####

#
# df = pd.read_pickle('ads_' + date_str + '.pkl')


df_existing = sql_ops.fetch_table_adds_detail()

df = TableUpdater.update_table(df_bd=df_existing, df_new=df)

pandas_gbq.to_gbq(df, 'adds.adds_detail', project_id=sql_ops.project_id, if_exists='append')


###### add first time