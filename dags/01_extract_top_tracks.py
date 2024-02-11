import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
from airflow.models.baseoperator import chain
from airflow import DAG

dag = DAG(dag_id='teste',schedule=None)

print('oi')
print(pd.DataFrame(data=[],columns=['Teste']))