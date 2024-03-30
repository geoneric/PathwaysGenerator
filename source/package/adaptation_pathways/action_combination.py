from .action import Action


class ActionCombination(Action):
    _actions: list[Action]

    def __init__(self, name: str, actions: list[Action]) -> None:
        super().__init__(name)
        self._actions = list(dict.fromkeys(actions))

        if len(self._actions) < 2:
            raise ValueError("At least two different(!) actions must be combined")

    def __repr__(self) -> str:
        return f'ActionCombination("{self.name}", {self.actions})'

    @property
    def actions(self) -> list[Action]:
        return self._actions
