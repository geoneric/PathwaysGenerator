"""
A sequenced action is ...

This module contains the implementation of the :py:class:`SequencedAction` class.
"""
from .action import Action


class SequencedAction(Action):
    """
    SequencedAction instances represent ...

    :param description: ...
    """

    def __init__(self, from_action: Action, to_action: Action) -> None:
        super().__init__(f"{from_action} | {to_action}")
        self._from_action = from_action
        self._to_action = to_action

    @property
    def from_action(self) -> Action:
        return self._from_action

    @property
    def to_action(self) -> Action:
        return self._to_action
