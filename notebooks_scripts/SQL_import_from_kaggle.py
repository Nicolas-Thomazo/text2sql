# %% [markdown]
# This notebook is used to import the data from kaggle to a sqlite database from there:
# https://www.kaggle.com/datasets/dillonmyrick/bike-store-sample-database/data

# %% imports
import sqlite3 as sql
from logging import FileHandler, StreamHandler, basicConfig, getLogger
from pathlib import Path

import plotly.express as px
import polars as pl
from sqlparse import format

# %% setups
basicConfig(
    level="INFO",
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        # FileHandler(__name__ + ".log"),
        StreamHandler(),
    ],
)
logger = getLogger("creation_de_la_base_de_donnees")

rawdata_path = Path("../data/raw")
processed_path = Path("../data/processed")
sql_queries_path = Path("../data/external")
db_path = processed_path / "bike_store.db"
db_uri = f"sqlite:///{db_path.resolve().as_posix()}"

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


# %% functions

from text2sql.sql_utils import insert_lines, optimize_query, save_as_sql

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

# %% test database
# creation de la base si elle n'existe pas
for file_name in file_names:
    query = f"SELECT * FROM {file_name};"
    print(pl.read_database_uri(query=query, uri=db_uri))

# %% analyse data (SQL queries)
up1 = (
    """Je veux le stock de chaque produit par magasin ordonné par magasin et produit"""
)
q1 = """
SELECT
    stores.store_name as store_name,
    categories.category_name as category_name,
    SUM(stocks.quantity) AS sum_qty
FROM stores
LEFT JOIN stocks ON stores.store_id = stocks.store_id
LEFT JOIN products ON stocks.product_id = products.product_id
LEFT JOIN categories ON products.category_id = categories.category_id
GROUP BY stores.store_name, categories.category_name
"""
up1b = """Je veux le stock de chaque produit par magasin ordonné par magasin et produit. pour chaque produit, je veux une ligne meme si le produit n'est pas dans le magasin"""
q1b = """
SELECT
    scq.store_name as store_name,
    scq.category_name as category_name,
    COALESCE(scq.sum_qty, 0) AS sum_qty
FROM (
    SELECT
        stores.store_name,
        categories.category_name
    FROM stores
    CROSS JOIN categories
) as sc
LEFT JOIN (
    SELECT
        stores.store_name as store_name,
        categories.category_name as category_name,
        SUM(stocks.quantity) AS sum_qty
    FROM stores
    LEFT JOIN stocks ON stores.store_id = stocks.store_id
    LEFT JOIN products ON stocks.product_id = products.product_id
    LEFT JOIN categories ON products.category_id = categories.category_id
    GROUP BY stores.store_name, categories.category_name
) AS scq ON sc.store_name = scq.store_name AND sc.category_name = scq.category_name
ORDER BY sc.store_name, sc.category_name;
"""
up2 = """Le nombre de commandes par magasin, par produit, ordonné par produit et magasin"""
q2 = """
SELECT
    categories.category_name,
    stores.store_name,
    SUM(order_items.quantity) AS sum_qty
FROM categories
JOIN products ON categories.category_id = products.category_id
JOIN order_items ON products.product_id = order_items.product_id
JOIN orders ON order_items.order_id = orders.order_id
JOIN stores ON orders.store_id = stores.store_id
GROUP BY stores.store_name, categories.category_name
ORDER BY categories.category_name, stores.store_name;
"""
up3 = (
    """La valeur totale des ventes par magasin, par mois, ordonné par magasin et mois"""
)
q3 = """
SELECT
    stores.store_name,
    STRFTIME('%Y %m', orders.order_date) AS year_month,
    SUM(order_items.quantity * order_items.list_price * (1 - order_items.discount)) AS total_price
FROM order_items
JOIN orders ON order_items.order_id = orders.order_id
JOIN stores ON orders.store_id = stores.store_id
GROUP BY stores.store_name, year_month
ORDER BY store_name, year_month;
"""
up4 = """Les 3 vendeurs qui ont le plus vendu en valeur par magasin et par mois"""
q4 = """
SELECT
    staffs.staff_id,
    staffs.first_name,
    staffs.last_name,
    stores.store_name,
    COUNT(orders.order_id) AS number_of_orders
FROM orders
LEFT JOIN staffs ON orders.staff_id = staffs.staff_id
LEFT JOIN stores ON staffs.store_id = stores.store_id
GROUP BY staffs.staff_id
HAVING number_of_orders >= (
    SELECT MIN(x)
    FROM (
        SELECT
            s.staff_id,
            s.first_name,
            s.last_name,
            COUNT(o.order_id) AS x
        FROM orders AS o
        JOIN staffs AS s ON o.staff_id = s.staff_id
        GROUP BY s.staff_id
        ORDER BY x DESC
        LIMIT 3)
    )
ORDER BY number_of_orders DESC
"""
up4b = """Les 3 vendeurs qui ont le plus vendu en nombre par magasin et par mois"""
q4b = """
SELECT
    staffs.staff_id,
    staffs.first_name,
    staffs.last_name,
    stores.store_name,
    COUNT(orders.order_id) AS number_of_orders
FROM orders
LEFT JOIN staffs ON orders.staff_id = staffs.staff_id
LEFT JOIN stores ON staffs.store_id = stores.store_id
GROUP BY staffs.staff_id
HAVING number_of_orders >= (
    SELECT MAX(x)
    FROM (
        SELECT
            s.staff_id,
            s.first_name,
            s.last_name,
            COUNT(o.order_id) AS x
        FROM orders AS o
        JOIN staffs AS s ON o.staff_id = s.staff_id
        GROUP BY s.staff_id
        ORDER BY x
        LIMIT 3)
    )
ORDER BY number_of_orders
"""
up5 = """les vendeurs qui ont le moins vendu en valeur par magasin et par mois"""
q5 = """
SELECT
    staffs.staff_id,
    staffs.first_name,
    staffs.last_name,
    stores.store_name,
    SUM(order_items.quantity * order_items.list_price * (1 - order_items.discount)) AS value_of_orders
FROM orders
LEFT JOIN staffs ON orders.staff_id = staffs.staff_id
LEFT JOIN stores ON staffs.store_id = stores.store_id
LEFT JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY staffs.staff_id
HAVING value_of_orders <= (
    SELECT MIN(x)
    FROM (
        SELECT
            s.staff_id,
            s.first_name,
            s.last_name,
            SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS x
        FROM orders AS o
        LEFT JOIN staffs AS s ON o.staff_id = s.staff_id
        LEFT JOIN order_items AS oi ON o.order_id = oi.order_id
        GROUP BY s.staff_id
        ORDER BY x DESC
        LIMIT 3)
    )
ORDER BY value_of_orders DESC
"""
up5 = """les vendeurs qui ont le moins vendu en nombre par magasin et par mois"""
q5b = """
SELECT
    staffs.staff_id,
    staffs.first_name,
    staffs.last_name,
    stores.store_name,
    SUM(order_items.quantity * order_items.list_price * (1 - order_items.discount)) AS value_of_orders
FROM orders
LEFT JOIN staffs ON orders.staff_id = staffs.staff_id
LEFT JOIN stores ON staffs.store_id = stores.store_id
LEFT JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY staffs.staff_id
HAVING value_of_orders <= (
    SELECT MAX(x)
    FROM (
        SELECT
            s.staff_id,
            s.first_name,
            s.last_name,
            SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS x
        FROM orders AS o
        LEFT JOIN staffs AS s ON o.staff_id = s.staff_id
        LEFT JOIN order_items AS oi ON o.order_id = oi.order_id
        GROUP BY s.staff_id
        ORDER BY x
        LIMIT 3)
    )
ORDER BY value_of_orders
"""

# %% making the dataframes
df1 = pl.read_database_uri(query=q1, uri=db_uri).with_columns(
    pl.col(["store_name", "category_name"]).cast(pl.Categorical)
)
df1b = pl.read_database_uri(query=q1b, uri=db_uri).with_columns(
    pl.col(["store_name", "category_name"]).cast(pl.Categorical)
)
df2 = pl.read_database_uri(query=q2, uri=db_uri).with_columns(
    pl.col(["store_name", "category_name"]).cast(pl.Categorical)
)
df3 = pl.read_database_uri(query=q3, uri=db_uri).with_columns(
    pl.col(["store_name", "year_month"]).cast(pl.Categorical)
)
df4 = pl.read_database_uri(query=q4, uri=db_uri).with_columns(
    pl.col(["staff_id"]).cast(pl.String).cast(pl.Categorical)
)
df4b = pl.read_database_uri(query=q4b, uri=db_uri).with_columns(
    pl.col(["staff_id"]).cast(pl.String).cast(pl.Categorical)
)
df5 = pl.read_database_uri(query=q5, uri=db_uri).with_columns(
    pl.col(["staff_id"]).cast(pl.String).cast(pl.Categorical)
)
df5b = pl.read_database_uri(query=q5b, uri=db_uri).with_columns(
    pl.col(["staff_id"]).cast(pl.String).cast(pl.Categorical)
)

# %% display data
print(df1)
print(df2)
print(df3)
print(df4)
print(df5)
print(df4b)
print(df5b)

# %% graph1
px.bar(
    df1.to_pandas(), x="category_name", y="sum_qty", color="store_name", barmode="group"
)
# %% graph1b
px.bar(
    df1b.to_pandas(),
    x="category_name",
    y="sum_qty",
    color="store_name",
    barmode="group",
)
# %% graph2
px.bar(
    df2.to_pandas(), x="store_name", y="sum_qty", color="category_name", barmode="group"
)
# %% graph3
px.line(df3.to_pandas(), x="year_month", y="total_price", color="store_name")
# %% graph4
px.bar(
    df4.with_columns(
        name=pl.concat_str("first_name", "last_name", separator=" ")
    ).to_pandas(),
    x="name",
    y="number_of_orders",
    color="store_name",
)
# %% graph4b
px.bar(
    df4b.with_columns(
        name=pl.concat_str("first_name", "last_name", separator=" ")
    ).to_pandas(),
    x="name",
    y="number_of_orders",
    color="store_name",
)
# %% graph5
px.bar(
    df5.with_columns(
        name=pl.concat_str("first_name", "last_name", separator=" ")
    ).to_pandas(),
    x="name",
    y="value_of_orders",
    color="store_name",
)
# %% graph5b
px.bar(
    df5b.with_columns(
        name=pl.concat_str("first_name", "last_name", separator=" ")
    ).to_pandas(),
    x="name",
    y="value_of_orders",
    color="store_name",
)
# %% Print formated SQL queries
print(format(q1, reindent=True, keyword_case="upper"))
print(format(q1b, reindent=True, keyword_case="upper"))
print(format(q2, reindent=True, keyword_case="upper"))
print(format(q3, reindent=True, keyword_case="upper"))
print(format(q4, reindent=True, keyword_case="upper"))
print(format(q5, reindent=True, keyword_case="upper"))
print(format(q4b, reindent=True, keyword_case="upper"))
print(format(q5b, reindent=True, keyword_case="upper"))
# %% optimize queries with sqlglot
# print(optimize_query(q1))
# print(optimize_query(q1b))
# print(optimize_query(q2))
# print(optimize_query(q3))
# print(optimize_query(q4))
# print(optimize_query(q4b))
# print(optimize_query(q5))
# print(optimize_query(q5b))

# %% export sql queries
save_as_sql(
    query=optimize_query(q1),
    file_name="query1.sql",
    folder=sql_queries_path,
    overwrite=True,
)
save_as_sql(
    query=optimize_query(q1b),
    file_name="query1b.sql",
    folder=sql_queries_path,
    overwrite=True,
)
save_as_sql(
    query=optimize_query(q2),
    file_name="query2.sql",
    folder=sql_queries_path,
    overwrite=True,
)
save_as_sql(
    query=optimize_query(q3),
    file_name="query3.sql",
    folder=sql_queries_path,
    overwrite=True,
)
save_as_sql(
    query=optimize_query(q4),
    file_name="query4.sql",
    folder=sql_queries_path,
    overwrite=True,
)
save_as_sql(
    query=optimize_query(q5),
    file_name="query5.sql",
    folder=sql_queries_path,
    overwrite=True,
)
save_as_sql(
    query=optimize_query(q4b),
    file_name="query4b.sql",
    folder=sql_queries_path,
    overwrite=True,
)
save_as_sql(
    query=optimize_query(q5b),
    file_name="query5b.sql",
    folder=sql_queries_path,
    overwrite=True,
)
# %% parsing examples
# from sqlglot import parse_one

# parse_one(q1, dialect="sqlite")
# parse_one(q1b[10:-10], dialect="sqlite")

# %% same thing with sqloxide
# from sqloxide import parse_sql

# parse_sql(q1b, dialect="sqlite")
# %%
