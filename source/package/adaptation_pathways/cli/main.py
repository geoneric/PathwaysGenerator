import sys
from typing import Callable


def main_function(function: Callable):
    def wrapper(*args, **kwargs) -> int:
        try:
            status = function(*args, **kwargs)
        except Exception as error:  # pylint: disable=broad-exception-caught
            sys.stderr.write(f"Error occurred:\n{str(error)}\n")
            status = 1

        return status

    return wrapper


def common_arguments() -> str:
    return """
    -h --help      Show this screen
    --version      Show version
"""
