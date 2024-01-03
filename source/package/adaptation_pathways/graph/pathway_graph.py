from .node import ActionConversion, ActionPeriod
from .rooted_graph import RootedGraph


class PathwayGraph(RootedGraph):
    """
    A PathwayGraph represents the dependencies between action sequences. The nodes represent
    the conversion from one action to another (think tipping points or vertical lines in a
    pathway map), and the edges the period of time a certain action is active (think horizontal
    lines in a pathway map).

    .. note::

       It is unclear ATM whether we actually need this class. Keep it for now and remove it
       once certain about it.
    """

    def add_conversion(
        self, from_action_period: ActionPeriod, to_action_period: ActionPeriod
    ) -> None:
        """
        Add a conversion, defined by two action periods
        """
        conversion = ActionConversion(from_action_period, to_action_period)
        self._graph.add_edge(from_action_period, conversion)
        self._graph.add_edge(conversion, to_action_period)

    def to_conversions(self, from_conversion: ActionPeriod) -> list[ActionConversion]:
        assert isinstance(from_conversion, ActionPeriod), type(from_conversion)
        return list(self._graph.adj[from_conversion])

    def to_action_period(self, conversion: ActionConversion) -> ActionPeriod:
        assert isinstance(conversion, ActionConversion), type(conversion)
        actions = list(self._graph.adj[conversion])
        assert len(actions) == 1
        assert isinstance(actions[0], ActionPeriod), type(actions[0])
        return actions[0]
