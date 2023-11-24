"""
A combined action is ...

This module contains the implementation of the :py:class:`CombinedAction` class.
"""
from .action import Action


class CombinedAction(Action):
    """
    CombinedAction instances represent ...

    :param actions: ...
    """

    _actions: list[Action]

    def __init__(self, actions: list[Action]) -> None:
        super().__init__(" + ".join([action.label for action in actions]))
        self._actions = actions

    @property
    def actions(self) -> list[Action]:
        return self._actions
