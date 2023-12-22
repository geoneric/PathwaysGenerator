from .action import Action
from .node import Node


class ActionBegin(Node):
    def __init__(self, action: Action) -> None:
        super().__init__(f"[{action.label}")
        self._action = action

    def __repr__(self) -> str:
        return f'ActionBegin("{self._label}")'

    def __hash__(self):
        return hash((self._action, self._label))

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self._action, self._label) == (
            other._action,
            other._label,
        )

    @property
    def action(self) -> Action:
        return self._action
