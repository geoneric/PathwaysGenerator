"""
A pathway is a sequence (or portfolio) of one or more interventions (AKA policy actions and
actions) over time, to achieve a set of pre-defined objectives under uncertain and changing
future conditions.

This module contains the implementation of the :py:class:`Pathway` class.
"""
from .intervention import Intervention


# TODO Is this maybe a ConditionBasedPathway? Is an Intervention maybe a
# ConditionBasedIntervention? → condition_based.pathway, condition_based.intervention vs
# time_based.pathway and time_based.intervention?


class Pathway:
    """
    Pathway instances represent a sequence of interventions.

    :param interventions: List of interventions that define the pathway
    """

    _interventions: list[Intervention]

    def __init__(self, interventions: list[Intervention]):
        self._interventions = interventions

    @property
    def interventions(self) -> list[Intervention]:
        return self._interventions

    def todo(self):
        pass
