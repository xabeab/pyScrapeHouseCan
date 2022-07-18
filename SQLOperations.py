
from google.cloud import bigquery
from google.oauth2 import service_account
import os
import pandas as pd

from queries import table_query

class SQLOperations:

    shema_add_details = {'fields': [{'name': 'index', 'type': 'integer'},
                                    {'name': 'id', 'type': 'string'},
                                    {'name': 'url', 'type': 'string'},
                                    {'name': 'current_date', 'type': 'string'},
                                    {'name': 'price', 'type': 'number'},
                                    {'name': 'isExchange', 'type': 'string'},
                                    {'name': 'location', 'type': 'string'},
                                    {'name': 'title', 'type': 'string'},
                                    {'name': 'description', 'type': 'string'},
                                    {'name': 'date_posted', 'type': 'string'},
                                    {'name': 'nearest_intersection_1', 'type': 'string'},
                                    {'name': 'nearest_intersection_2', 'type': 'string'},
                                    {'name': 'nb_bedrooms', 'type': 'string'},
                                    {'name': 'first_extracted', 'type': 'string'},
                                    {'name': 'last_extracted', 'type': 'string'}
                                    ],
                         'pandas_version': '1.4.0'}

    shema_add_details_1 = {'fields': [{'name': 'index', 'type': 'integer'},
                {'name': 'id', 'type': 'string'},
                {'name': 'url', 'type': 'string'},
                {'name': 'current_date', 'type': 'datetime', 'tz': 'UTC'},
                {'name': 'price', 'type': 'number'},
                {'name': 'isExchange', 'type': 'boolean', 'extDtype': 'boolean'},
                {'name': 'location', 'type': 'string'},
                {'name': 'title', 'type': 'string'},
                {'name': 'description', 'type': 'string'},
                {'name': 'date_posted', 'type': 'string'},
                {'name': 'nearest_intersection_1', 'type': 'string'},
                {'name': 'nearest_intersection_2', 'type': 'string'},
                {'name': 'nb_bedrooms', 'type': 'string'},
                {'name': 'first_extracted', 'type': 'datetime', 'tz': 'UTC'},
                {'name': 'last_extracted', 'type': 'datetime', 'tz': 'UTC'}],
     'primaryKey': ['index'],
     'pandas_version': '1.4.0'}

    def __init__(self) -> None:

        self.key_path = 'kijijidatabase-6414a390d2b7.json'

        self.credentials = service_account.Credentials.from_service_account_file(self.key_path,
                                                                                  scopes=["https://www.googleapis.com/auth/cloud-platform"]
                                                                                  )

        self.project_id = self.credentials.project_id

    def get_client(self) -> bigquery.Client:

        client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id,)

        return client

    def fetch_table_adds_detail(self) -> pd.DataFrame:

        df = (self.get_client().query(table_query).result().to_dataframe(create_bqstorage_client=True))

        return df

