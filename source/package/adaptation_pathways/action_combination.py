from .action import Action


class ActionCombination(Action):
    _actions: list[Action]

    def __init__(self, name: str, actions: list[Action], edition: int = 0) -> None:
        super().__init__(name, edition)
        self._actions = list(dict.fromkeys(actions))

        if len(self._actions) < 2:
            raise ValueError("At least two different(!) actions must be combined")

    def __repr__(self) -> str:
        return f'ActionCombination("{self.name}", {self.actions}, {self.edition})'

    @property
    def actions(self) -> list[Action]:
        return self._actions
