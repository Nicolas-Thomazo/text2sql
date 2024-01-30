"""
this module contains function to format and validate sql queries
"""

from pathlib import Path
from typing import Optional

from polars import DataFrame
from polars.type_aliases import DbWriteMode
from pydantic import ValidationError
from sqlalchemy import Engine, create_engine
from sqlalchemy.schema import MetaData
from sqlglot import ParseError, parse_one
from sqlglot.optimizer import optimize
from sqlparse import format

from text2sql import logger
from text2sql.format_utils import format_table_description
from text2sql.types import SQLUrl


def check_uri(uri: str) -> SQLUrl:
    try:
        return SQLUrl(uri)
    except ValidationError as e:
        logger.error(f"{e}: when trying to connect to {uri}")
        raise e


def insert_lines(
    connection_uri_string: str,
    df: DataFrame,
    table_name: str,
    if_exists: DbWriteMode = "replace",
) -> None:
    uri = check_uri(connection_uri_string)

    nb_of_row_inserted = df.write_database(
        table_name=table_name,
        connection=uri.__str__(),
        if_table_exists=if_exists,
        engine="adbc",
    )
    logger.info(f"INSERT: {nb_of_row_inserted} rows inserted in {table_name}")


def get_db_schema(connection_uri_string: str) -> str:
    uri = check_uri(connection_uri_string)
    engine: Engine = create_engine(uri.__str__())
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return "\n".join(
        [format_table_description(table) for table in metadata.tables.values()]
    )


def get_sqlglot_schema(connection_uri_string: str) -> dict[str, dict[str, str]]:
    uri = check_uri(connection_uri_string)
    engine: Engine = create_engine(uri.__str__())
    metadata = MetaData()
    metadata.reflect(bind=engine)
    schema = {
        table.name: {column.name: column.type.__str__() for column in table.columns}
        for table in metadata.tables.values()
    }
    return schema


def save_as_sql(
    query: str, file_name: str, folder: Path = Path("."), overwrite: bool = False
) -> None:
    destination_file = folder / file_name
    if destination_file.exists() and not overwrite:
        raise FileExistsError(
            f"{destination_file} already exists, please use overwrite=True to overwrite it"
        )

    with open(destination_file, "w") as file:
        file.write(format(query, reindent=True, keyword_case="upper"))


def validate_sql_query(query: str, dialect: str = "sqlite") -> bool:
    try:
        parse_one(query, dialect=dialect)
        return True
    except ParseError as e:
        logger.info(f"{e}: when trying to validate {query}")
        return False


def optimize_query(query: str, connection_uri: Optional[str] = None) -> str:
    if connection_uri is None:
        return optimize(query).sql(pretty=True)

    uri = check_uri(connection_uri)
    dialect = uri.__str__().split(":")[0].lower()
    schema = get_sqlglot_schema(uri.__str__())

    return optimize(query, dialect=dialect, schema=schema).sql(pretty=True)
