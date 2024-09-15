# dbt-Airflow

After running 
```bash
docker compose up -d
```
(the `-d` flag here is for "detach" so that you can run other commands in the same terminal) 

Here it can be helpful for debugging to check:
```bash
docker compose logs -f airflow
```
to understand what happened if airflow crashed.

## Notes

This project uses docker compose to orchestrate two containers:
- a postgres container for the star database,
- an airflow container, in which `dbt` is installed by default.

which are brought up (in the above order) via `docker compose up -d`. The log command `docker compose logs -f airflow` provides a link to the airflow webserver after the initialization process runs successfully. 

Airflow runs a very simple DAG which executes `dbt build` and `dbt docs generate` and `dbt docs serve`. The `dbt docs serve` task should probably be a separate service, but this is just for tinkering anyway.

## Resolving potential issues

- Permissions may have to be adjusted for the `dbt_project/dbt/target` folder in order for the `dbt docs generate` command to run successfully in the airflow container. For this, just run:
  
    ```bash
    chmod -R 775 dbt_project/dbt/target
    ```
  
    before starting the containers.

- Airflow requires sqlalchemy < 2.0, but the `import_data.py` script uses sqlalchemy > 2.0. This is just for loading data into postgres anyway, so not really the source of any major issues, just something to be aware of.