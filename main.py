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
from PageParser import parse_kijiji
import pandas as pd
import os



if __name__ == "__main__":

    url = 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/c37l1700281?ad=offering'

    df = parse_kijiji(url)

    # Save pkl file
    date_str = str(date.today())
    df.to_pickle('ads_' + date_str + '.pkl')

    ## CREATE FIRST TABLE

    sql_ops = SQLOperations()

    # Drop duplicates rows
    cols_to_compare = ['price', 'title', 'date_posted', 'nb_bedrooms',  'nearest_intersection_1', 'nearest_intersection_2', 'nb_bedrooms']
    df = df.drop_duplicates(subset=cols_to_compare)

    # pandas_gbq.to_gbq(df_0, 'adds.adds_detail', project_id=sql_ops.project_id, if_exists='replace', table_schema=sql_ops.shema_add_details_1)
    # df = pd.read_pickle('ads_' + date_str + '.pkl')

    # Fetch existing data
    df_existing = sql_ops.fetch_table_adds_detail()

    # Filter to keep only new adds
    df = TableUpdater.update_table(df_bd=df_existing, df_new=df)

    # Convert columns to datetime
    cols_to_date = ['current_date', 'first_extracted', 'last_extracted']
    for col in cols_to_date:
        df[col] = pd.to_datetime(df[col], utc=True)

    # Convert other column to proper schema
    df = df.astype(df_existing.dtypes)

    print(f'Appending {df.shape[0]} new adds to adds_detail table')

    # Update remote db with new adds
    pandas_gbq.to_gbq(df, 'adds.adds_detail', project_id=sql_ops.project_id, if_exists='append')
