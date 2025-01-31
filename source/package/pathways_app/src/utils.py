from typing import Callable, TypeVar


T = TypeVar("T")


def find_index(element_list: list[T], pred: Callable[[T], bool]) -> int | None:
    for index, value in enumerate(element_list):
        if pred(value):
            return index
    return None
