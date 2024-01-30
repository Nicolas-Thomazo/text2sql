"""
this module contains function to format and validate sql queries
"""

from sqlalchemy.schema import Table


def format_table_description(table: Table) -> str:
    table_columns = [f"{column.name}:{column.type}" for column in table.columns]
    return f"{table.name} ({', '.join(table_columns)})"
