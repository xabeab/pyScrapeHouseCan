
from google.cloud import bigquery
from google.oauth2 import service_account
import os
import pandas as pd

from queries import table_query

class SQLOperations:

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

