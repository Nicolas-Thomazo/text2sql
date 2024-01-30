from typing import Callable

from fastapi import FastAPI


def preload_for_each_worker():
    """
    In order to load something in memory to each worker
    """
    # from something import SomeClass

    # SomeClass.get_data()
    pass


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        preload_for_each_worker()

    return start_app
