import pandas as pd

class TableUpdater:

    def update_table(df_bd: pd.DataFrame, df_new: pd.DataFrame) -> pd.DataFrame:
        # Create set of ids
        set_ids_bd = set(df_bd['id'])
        set_ids_new = set(df_new['id'])

        # Create bool to select which row to update in main db and which row to append to db
        id_to_update = set_ids_bd.intersection(set_ids_new)
        se_bool_to_update = df_new['id'].isin(id_to_update)

        # Create dfs to perform both operations
        df_to_update = df_new.loc[se_bool_to_update, :].copy()
        df_to_add = df_new.loc[se_bool_to_update == False, :].copy()

        # Update existing add in exiting table
        df_bd = update_existing_adds(df_bd, df_to_update)

        # Add new adds to main database
        df_bd = add_new_adds(df_bd, df_to_add)

        return df_bd


    def update_existing_adds(df_bd: pd.DataFrame, df_new: pd.DataFrame) -> pd.DataFrame:
        df = pd.merge(left=df_bd, right=df_new, how='left', on='id', suffixes=('', '_y'))

        # Create a series of bool indicating if the add already exist in the database
        se_bool_already_existing = df['last_extracted_y'].isna() == False

        # To existing adds, update the last extracted date
        df.loc[se_bool_already_existing, 'last_extracted'] = df.loc[se_bool_already_existing, 'last_extracted_y'].values

        # Update time extracted
        df.loc[se_bool_already_existing, 'time_open'] = df.loc[se_bool_already_existing, 'last_extracted'] - df.loc[
            se_bool_already_existing, 'first_extracted']

        df = df.loc[:, df_bd.columns].copy()

        return df


    def add_new_adds(df_bd: pd.DataFrame, df_new: pd.DataFrame) -> pd.DataFrame:
        df = pd.concat([df_bd, df_new], axis=0)

        return df