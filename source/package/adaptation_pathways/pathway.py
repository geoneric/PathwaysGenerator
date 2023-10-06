# Pathways are sequences (or portfolios) of actions / interventions over time to achieve a set
# of pre-defined objectives under uncertain and changing future conditions.

from .intervention import Intervention


class Pathway:
    _interventions: list[Intervention]

    def __init__(self):
        self._interventions = []

    @property
    def interventions(self) -> list[Intervention]:
        return self._interventions

    def todo(self):
        pass
