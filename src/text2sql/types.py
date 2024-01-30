"""
this module contains types aliases
"""

from typing import Annotated

from pydantic.networks import AnyUrl, UrlConstraints

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
