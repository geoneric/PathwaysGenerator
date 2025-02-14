from ...action import Action
from .node import Node


class ActionEnd(Node):
    """
    A node representing the end of an action

    :param action: Action this node is the end of

    See also: :class:`PathwayMap`
    """

    def __init__(self, action: Action) -> None:
        super().__init__(f"{action.name}]")
        self._action = action

    def __repr__(self) -> str:
        return f'ActionEnd("{self._action}")'

    @property
    def action(self) -> Action:
        return self._action
