from .action import Action
from .node import Node


class ActionPeriod(Node):
    def __init__(self, action: Action) -> None:
        super().__init__(f"{action.label}")
        self._action = action

    def __repr__(self) -> str:
        return f'ActionPeriod("{self._action}")'

    @property
    def action(self) -> Action:
        return self._action
