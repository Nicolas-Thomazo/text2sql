# %% imports
import sqlite3 as sql
from logging import StreamHandler, basicConfig, getLogger
from pathlib import Path
from typing import Annotated

import polars as pl
from pydantic.networks import AnyUrl, UrlConstraints

from text2sql.ai_utils import chatbot_SQL_query, clarify_user_request, create_prompt
from text2sql.sql_utils import get_db_schema, insert_lines

# %% setups
basicConfig(
    level="INFO",
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        StreamHandler(),
    ],
)
logger = getLogger("creation_de_la_base_de_donnees")

rawdata_path = Path("../data/raw")
processed_path = Path("../data/processed")
sql_queries_path = Path("../data/external")
db_path = processed_path / "bike_store.db"
db_uri = f"sqlite:///{db_path.resolve().as_posix()}"

SQLUrl = Annotated[
    AnyUrl,
    UrlConstraints(
        allowed_schemes=[
            "mariadb",
            "mariadb+mariadbconnector",
            "mariadb+pymysql",
            "mysql",
            "mysql+mysqlconnector",
            "mysql+aiomysql",
            "mysql+asyncmy",
            "mysql+mysqldb",
            "mysql+pymysql",
            "mysql+cymysql",
            "mysql+pyodbc",
            "postgres",
            "postgresql",
            "postgresql+asyncpg",
            "postgresql+pg8000",
            "postgresql+psycopg",
            "postgresql+psycopg2",
            "postgresql+psycopg2cffi",
            "postgresql+py-postgresql",
            "postgresql+pygresql",
            "sqlite",
        ]
    ),
]
file_names = [
    "brands",
    "categories",
    "customers",
    "order_items",
    "orders",
    "products",
    "staffs",
    "stocks",
    "stores",
]

# %% import data (using globals... don't do that)
for file_name in file_names:
    logger.info(f"Importing {file_name}")
    globals()[file_name] = pl.read_csv(rawdata_path / f"{file_name}.csv")

# %% create database (using globals... don't do that)
db = sql.connect(database=db_path)
db.close()

for file_name in file_names:
    insert_lines(
        connection_uri_string=db_uri, df=globals()[file_name], table_name=file_name
    )

# %% make prompts

schema = get_db_schema(db_uri)
request = "give me the stocks in each store and for each category ordered by store and category"

logger.info(f"Query prompt for {request}")
logger.info(create_prompt(request, schema))
logger.info(f"Clarify prompt for {request}")
logger.info(clarify_user_request(request, schema))
logger.info(f"Chatbot prompt for {request}")
logger.info(chatbot_SQL_query(request, schema))

# %%
