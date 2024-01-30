import logging
import sys
from logging import getLogger

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.0"
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="")
DEBUG: bool = config("LOG_LEVEL", cast=str, default="INFO") == "DEBUG"
PROJECT_NAME: str = config("PROJECT_NAME", default="Text2SQL")

logger = getLogger("text2sql")
