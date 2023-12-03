import sys
import traceback
from typing import Callable


def common_arguments() -> str:
    return """\
    -h --help      Show this screen
    --version      Show version"""


def main_function(function: Callable):
    def wrapper(*args, **kwargs) -> int:
        try:
            status = function(*args, **kwargs)
        except Exception as error:  # pylint: disable=broad-exception-caught
            # TODO Only print traceback when some --verbose or --debug option is passed
            traceback.print_exception(error)
            # /TODO

            sys.stderr.write(f"Error occurred:\n{str(error)}\n")
            status = 1

        return status

    return wrapper
