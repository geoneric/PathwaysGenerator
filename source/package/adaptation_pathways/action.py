"""
An action (AKA policy action, intervention, and measure) is ...

This module contains the implementation of the :py:class:`Action` class.
"""


class Action:
    """
    Action instances represent ...
    """

    _name: str
    _edition: int

    def __init__(self, name: str, edition: int = 0) -> None:
        self._name = name
        self._edition = edition

    def __repr__(self) -> str:
        return f'Action("{self._name}", {self._edition})'

    def __lt__(self, other) -> bool:
        return hash(self) < hash(other)

    @property
    def name(self) -> str:
        return self._name

    @property
    def edition(self) -> int:
        return self._edition
