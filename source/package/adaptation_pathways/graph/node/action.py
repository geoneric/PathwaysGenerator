"""
An action (AKA policy action, intervention, and measure) is ...

This module contains the implementation of the :py:class:`Action` class.
"""
from .node import Node


class Action(Node):
    """
    Action instances represent ...

    :param label: Label of the action
    """

    def __repr__(self) -> str:
        return f'Action("{self._label}")'
