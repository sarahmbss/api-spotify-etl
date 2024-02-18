from datetime import datetime, timedelta
import pandas as pd

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator

from Spotify import Spotify
from ProcessData import Processing

with DAG(
     dag_id="etl-mysql-tbl-top-tracks"
    ,start_date=datetime(2024, 2, 18)
    ,max_active_runs=1
    ,schedule_interval=timedelta(hours=24)
    ,catchup=False
    ,tags=['etl','mysql','top_tracks']
) as dag:
    
    init = DummyOperator(task_id='init')

    get_data_api = PythonOperator(
         task_id='get_top_tracks_api'
        ,python_callable=Spotify.get_top_tracks
        ,provide_context=True
        ,op_kwargs={'limit': 50, 'time_range': 'short_term'}
    )

    clean_data = PythonOperator(
         task_id='clean_insert_data_mysql'
        ,python_callable=Processing.clean_user_top_tracks
        ,provide_context=True
    )

    finish = DummyOperator(task_id='finish')

    init >> get_data_api >> clean_data >> finish