"""
A scenario is ...

This module contains the implementation of the :py:class:`Scenario` class.
"""


# TODO ConditionBasedScenario? condition_based.scenario?
# TODO start_time is determined by the min of range of changing condition being considered


class Scenario:
    """
    Scenario instances ...
    """

    _name: str
    _start: tuple[int, float]
    _end: tuple[int, float]

    def __init__(
        self,
        name: str,
        start: tuple[int, float],
        end: tuple[int, float],
    ):
        assert start[0] < end[0]
        assert start[1] < end[1]

        self._name = name

    @property
    def name(self) -> str:
        """
        Name of the scenario
        """
        return self._name

    @property
    def start(self) -> tuple[int, float]:
        return self._start

    @property
    def end(self) -> tuple[int, float]:
        return self._end
