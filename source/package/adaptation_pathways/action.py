"""
An action (AKA policy action, intervention, and measure) is ...

This module contains the implementation of the :py:class:`Action` class.
"""


class Action:
    """
    Action instances represent ...
    """

    _name: str

    def __init__(self, name: str) -> None:
        self._name = name

    def __str__(self) -> str:
        return f"{self._name}"

    def __repr__(self) -> str:
        return f'Action("{self._name}")'

    def __lt__(self, other) -> bool:
        return hash(self) < hash(other)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name
