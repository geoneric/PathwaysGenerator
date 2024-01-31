from ...action import Action as Action_
from .node import Node


class Action(Node):
    def __init__(self, action: Action_) -> None:
        super().__init__(f"{action.name}")
        self._action = action

    def __repr__(self) -> str:
        return f'Action("{self._action}")'

    @property
    def action(self) -> Action_:
        return self._action
