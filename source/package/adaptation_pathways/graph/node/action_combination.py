from .action import Action


# Although only two actions can be combined into a single ActionCombination instance, the
# implementation allows this to be easily changed so that any number of actions can be combined.


class ActionCombination(Action):
    def __init__(self, label: str, action1: Action, action2: Action) -> None:
        super().__init__(label)
        self._actions = list(dict.fromkeys([action1, action2]))

        if len(self._actions) < 2:
            raise ValueError("At least two different(!) actions must be combined")

    def __repr__(self) -> str:
        # pylint: disable-next=consider-using-f-string
        return 'ActionCombination("{}", {})'.format(
            self.label, ", ".join([f'"{action.label}"' for action in self._actions])
        )

    @property
    def actions(self) -> list[Action]:
        return self._actions
