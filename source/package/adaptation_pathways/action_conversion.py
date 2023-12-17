"""
An ActionConversion is ...

This module contains the implementation of the :py:class:`ActionConversion` class.
"""
from .action import Action


class ActionConversion:
    """
    ActionConversion instances represent the moment that one action stops and another action
    begins

    :param label: Label of the conversion
    :param from_action: Previous / old action
    :param to_action: Next / new action
    """

    def __init__(self, from_action: Action, to_action: Action) -> None:
        self._label = f"{from_action} | {to_action}"
        self._from_action = from_action
        self._to_action = to_action

    def __str__(self) -> str:
        return self._label

    def __repr__(self) -> str:
        return f'ActionConversion("{self._label}")'

    @property
    def label(self) -> str:
        return self._label

    @property
    def from_action(self) -> Action:
        return self._from_action

    @property
    def to_action(self) -> Action:
        return self._to_action
