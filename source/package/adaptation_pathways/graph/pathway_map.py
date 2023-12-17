from ..action import Action
from .rooted_graph import RootedGraph


class PathwayMap(RootedGraph):
    """
    A PathwayMap represents a collection of adaptation pathways. These pathways are encoded
    in a directed rooted graph in which the nodes represent the tipping points, and the edges
    the period of time an action is active.

    The information in this graph is very similar to the information in a pathways graph,
    but for the sake of visualizing a pathways map, additional nodes are added to the graph.
    """

    def add_action(self, from_tipping_point: Action, to_tipping_point: Action) -> None:
        """
        Add an action, defined by two tipping points
        """
        self._graph.add_edge(from_tipping_point, to_tipping_point)

    def nr_downstream_actions(self, from_tipping_point: Action) -> int:
        return self._graph.out_degree(from_tipping_point)

    def to_tipping_point(self, from_tipping_point: Action) -> Action:
        out_edges = list(self._graph.out_edges(from_tipping_point))
        assert len(out_edges) == 1, out_edges
        return out_edges[0][1]

    def from_tipping_points(self, to_tipping_point: Action) -> list[Action]:
        return list(self._graph.adj[to_tipping_point])
