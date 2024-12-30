from datetime import datetime, timedelta
import pandas as pd

from airflow.operators.empty import EmptyOperator
from airflow.decorators import dag, task

from util import Util

@dag(
     dag_id="etl-mysql-tbl-top-tracks"
    ,start_date=datetime(2024, 12, 29)
    ,max_active_runs=1
    ,schedule_interval=timedelta(hours=24)
    ,catchup=False
    ,tags=['etl','mysql','user_top_tracks']
)

def etl_tbl_top_tracks() -> None:
    '''
    Description:
        - Responsible to control the execution flow of this DAG
    '''
    
    start = EmptyOperator(task_id='start')

    @task
    def get_user_top_tracks(_limit: int, _time_range: str) -> dict:
        '''
        Description: 
            - Get the most listened tracks by the user

        Arguments:
            - limit: number of songs that will be searched
            - time_range: number of months to be considered
        '''
        spot_credential = Util.get_spotify_credential()
        top_tracks = spot_credential.current_user_top_tracks(limit=_limit, offset=0, time_range=_time_range)['items']  
        return top_tracks

    @task
    def clean_user_top_tracks() -> None:
        '''
        Description: 
            - Clean API response and upload it on the database
        '''

        df = pd.DataFrame([], columns=['song_id','song_name','artist_name','album_name','popularity','uri'])

        for song in top_tracks['items']:
            df.loc[-1] = [song['id'],song['name'],song['artists'][0]['name'],song['album']['name'],song['popularity'],song['uri']]
            df.reset_index(inplace=True, drop=True)

        print(df.head())

        Util.insert_df_mysql(df, 'user_top_tracks')

    finish = EmptyOperator(task_id='finish')

    top_tracks = get_user_top_tracks(50, 'short_term')
    clean_top_tracks = clean_user_top_tracks()

    start >> top_tracks >> clean_top_tracks >> finish

etl_tbl_top_tracks()