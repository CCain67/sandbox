import pandas as pd
from sqlalchemy import create_engine

# connect to the postgres database (postgresql://<username>:<password>@<host>/<database_name>)
engine = create_engine("postgresql://postgres:postgres@172.19.0.3:5432/my_db")

# read and insert
pd.read_csv("data/stars.csv").to_sql(
    "stars", engine, if_exists="replace", index=False, method="multi"
)
