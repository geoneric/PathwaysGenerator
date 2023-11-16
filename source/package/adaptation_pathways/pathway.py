"""
A pathway is a sequence (or portfolio) of one or more actions over time, to achieve a set of
pre-defined objectives under uncertain and changing future conditions.

This module contains the implementation of the :py:class:`Pathway` class.
"""
from .action import Action


class Pathway:
    """
    Pathway instances represent a sequence of actions.

    :param actions: List of actions that define the pathway
    :param tipping_points: The time points after which each action is not sufficient any
        more. The value is directly related to the changing condition (e.g. sedimentation rate)
        being considered.

    A pathway defines the tipping point of actions. For example:

    Action 1: Current situation, do  nothing
    Action 2: Increase dike crest levels by 0.5m
    Action 3: Create more room for the river by adding 1km of floodplains
    Action 4: Ring dikes around population centers
    """

    _actions: list[Action]

    def __init__(self, actions: list[Action]):
        self._actions = actions

    @property
    def actions(self) -> list[Action]:
        return self._actions

    def todo(self):
        pass
