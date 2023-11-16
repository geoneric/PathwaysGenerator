"""
A combined action is ...

This module contains the implementation of the :py:class:`CombinedAction` class.
"""
from .action import Action


class CombinedAction(Action):
    """
    CombinedAction instances represent ...

    :param description: ...
    """

    _actions: list[Action]

    def __init__(self, actions: list[Action]) -> None:
        super().__init__(" + ".join([action.description for action in actions]))
        self._actions = actions

    @property
    def actions(self) -> list[Action]:
        return self._actions
