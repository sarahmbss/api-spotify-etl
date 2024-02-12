import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
from airflow.models.baseoperator import chain
from airflow import DAG
from airflow.operators.dummy import DummyOperator


@dag(
    dag_id="teste",
)

# init main function
def load_data():

    # init task
    init_data_load = DummyOperator(task_id="init")

    # finish task
    finish_data_load = DummyOperator(task_id="finish")

    # define sequence
    init_data_load >> finish_data_load


# init dag
dag = load_data()