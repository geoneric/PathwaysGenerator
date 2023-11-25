from .action import Action
from .rooted_graph import RootedGraph


class PathwaysMap(RootedGraph):
    """
    A PathwaysMap represents a collection of adaptation pathways. These pathways are encoded
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

    def nr_pathways(self, from_tipping_point: Action) -> int:
        return self._graph.out_degree(from_tipping_point)
