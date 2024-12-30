import pandas as pd
import sqlalchemy, os

import spotipy
import spotipy.util as util

class Util:

    @staticmethod
    def get_spotify_credential():
        CLIENT_ID = os.getenv("CLIENT_ID_ENV")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET_ENV")
        USERNAME = os.getenv("USERNAME_ENV")
        SCOPE = os.getenv("SCOPE_ENV")
        REDIRECT_URL = os.getenv("REDIRECT_URL_ENV")
        token = util.prompt_for_user_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, scope=SCOPE, redirect_uri=REDIRECT_URL)
        spot = spotipy.Spotify(auth=token)
        return spot

    @staticmethod
    def insert_df_mysql(df: pd.DataFrame, table: str):
        engine = sqlalchemy.create_engine(f'mysql+pyodbc://{os.getenv("UID_ENV")}:{os.getenv("PWD_ENV")}@{os.getenv("HOST_ENV")}:3306/{os.getenv("DATABASE_ENV")}')
        df.to_sql(name=table, con=engine, if_exists = 'append', index=False)