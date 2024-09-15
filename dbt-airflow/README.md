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

This project uses docker compose to orchestrate 3 containers:
- a postgres container for the star database
- a python 3.11 container with `dbt-postgres` installed
- an airflow container

which are brought up (in the above order)

## Resolving potential issues

Permissions may have to be adjusted for the `dbt_project/dbt/target` folder in order for the `dbt docs generate` command to run successfully in the airflow container. For this, just run:
```bash
chmod -R 775 dbt_project/dbt/target
```

