"""
An action (AKA policy action, intervention, and measure) is ...

This module contains the implementation of the :py:class:`Action` class.
"""


class Action:
    """
    Action instances represent ...

    :param label: Label of the action
    """

    _label: str

    def __init__(self, label: str) -> None:
        self._label = label

    def __str__(self) -> str:
        return self._label

    def __repr__(self) -> str:
        return f'Action("{self._label}")'

    @property
    def label(self) -> str:
        return self._label
