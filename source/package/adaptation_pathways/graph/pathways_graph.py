from ..action import Action
from .rooted_graph import RootedGraph


class PathwaysGraph(RootedGraph):
    """
    A PathwaysGraph represents the dependencies between action sequences. The nodes represent
    the conversion from one action to another (think tipping points or vertical lines in a
    pathways map), and the edges the period of time a certain action is active (think horizontal
    lines in a pathways map).
    """

    def add_action(self, from_tipping_point: Action, to_tipping_point: Action) -> None:
        """
        Add an action, defined by two tipping points
        """
        self._graph.add_edge(from_tipping_point, to_tipping_point)

    def nr_to_tipping_points(self, from_tipping_point: Action) -> int:
        return self._graph.out_degree(from_tipping_point)

    def to_tipping_points(self, from_tipping_point: Action) -> list[Action]:
        return list(self._graph.adj[from_tipping_point])
