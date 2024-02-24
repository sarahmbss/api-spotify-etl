import pandas as pd
from operator import itemgetter
import sqlalchemy
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Processing:

    def insert_df_mysql(self, df: pd.DataFrame, table: str):
        engine = sqlalchemy.create_engine(f'mysql+pyodbc://{config['BANCO']['UID']}:{config['BANCO']['PWD']}@{config['BANCO']['HOST']}:3306/{config['BANCO']['DATABASE']}')
        df.to_sql(name=table, con=engine, if_exists = 'append', index=False)

    def clean_user_top_tracks(self, ti):
        top_tracks = ti.xcom_pull(task_ids=['get_top_tracks_api'],key='user_top_tracks')

        df = pd.DataFrame([], columns=['song_id','song_name','artist_name','album_name','popularity','uri'])

        for song in top_tracks['items']:
            df.loc[-1] = [song['id'],song['name'],song['artists'][0]['name'],song['album']['name'],song['popularity'],song['uri']]
            df.reset_index(inplace=True, drop=True)

        self.insert_df_mysql(df, 'user_top_tracks')