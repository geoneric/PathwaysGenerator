"""
A pathway is a sequence (or portfolio) of one or more actions over time, to achieve a set of
pre-defined objectives under uncertain and changing future conditions.

This module contains the implementation of the :py:class:`Pathway` class.
"""
from .action import Action


# TODO Is this maybe a ConditionBasedPathway? Is an Action maybe a
# ConditionBasedIntervention? → condition_based.pathway, condition_based.action vs
# time_based.pathway and time_based.action?


# Pathways can be compared according to scores:
# - target effects (benefits?)
# - costs
# - side effect (pos and neg?)


class Pathway:
    """
    Pathway instances represent a sequence of actions.

    :param actions: List of actions that define the pathway
    """

    _actions: list[Action]

    def __init__(self, actions: list[Action]):
        self._actions = actions

    @property
    def actions(self) -> list[Action]:
        return self._actions

    def todo(self):
        pass
