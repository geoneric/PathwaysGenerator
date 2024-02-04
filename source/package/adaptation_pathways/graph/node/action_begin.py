from ...action import Action
from .node import Node


class ActionBegin(Node):
    _action: Action

    def __init__(self, action: Action) -> None:
        super().__init__(f"[{action.name}")
        self._action = action

    def __repr__(self) -> str:
        return f'ActionBegin("{self._action}")'

    @property
    def action(self) -> Action:
        return self._action
