from .action import Action


class ActionEnd:
    _label: str

    def __init__(self, action: Action) -> None:
        self._action = action
        self._label = f"{action.label}]"

    def __str__(self) -> str:
        return self._label

    def __repr__(self) -> str:
        return f'ActionEnd("{self._label}")'

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

    @property
    def label(self) -> str:
        return self._label
