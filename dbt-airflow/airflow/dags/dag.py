from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "start_date": datetime.today(),
}

dag = DAG(
    "dbt_dag",
    default_args=default_args,
    schedule_interval="*/5 * * * *",
    catchup=False,
)

dbt_run = BashOperator(
    task_id="dbt_run",
    bash_command="dbt build --target=dev --profiles-dir /workspace/dbt_project/dbt --project-dir /workspace/dbt_project/dbt",
    dag=dag,
)
