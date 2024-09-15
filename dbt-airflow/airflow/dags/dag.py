from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "start_date": datetime.today(),
}

with DAG(
    "dbt_dag",
    default_args=default_args,
    schedule_interval="*/5 * * * *",
    catchup=False,
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_build",
        bash_command="dbt build --target=dev --profiles-dir /workspace/dbt_project/dbt --project-dir /workspace/dbt_project/dbt",
        dag=dag,
    )

    dbt_docs_gen = BashOperator(
        task_id="dbt_docs_gen",
        bash_command="dbt docs generate --target=dev --profiles-dir /workspace/dbt_project/dbt --project-dir /workspace/dbt_project/dbt",
        dag=dag,
    )

    dbt_docs_serve = BashOperator(
        task_id="dbt_docs_serve",
        bash_command="dbt docs serve --port 8081 --target=dev --profiles-dir /workspace/dbt_project/dbt --project-dir /workspace/dbt_project/dbt",
        dag=dag,
    )

    dbt_run >> dbt_docs_gen >> dbt_docs_serve
