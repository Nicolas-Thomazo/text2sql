"""
init of the package: setup logging for the package
"""

from logging import FileHandler, StreamHandler, basicConfig, getLogger

from dotenv import dotenv_values

config = dotenv_values(".env")

basicConfig(
    level=config.get("LOG_LEVEL", "INFO"),
    format=config.get("LOG_FORMAT", "%(asctime)s %(levelname)s %(message)s"),
    handlers=[FileHandler(config.get("LOG_NAME", __name__) + ".log"), StreamHandler()],
)
logger = getLogger("text2sql")

__author__ = """Guillaume Lombardo"""
__email__ = """guillaume.lombardo@banque-france.fr"""
__version__ = """0.1.0"""
