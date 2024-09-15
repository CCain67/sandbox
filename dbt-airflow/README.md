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

