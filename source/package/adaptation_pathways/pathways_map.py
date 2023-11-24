from .rooted_graph import RootedGraph


class PathwaysMap(RootedGraph):
    """
    A PathwaysMap represents a collection of adaptation pathways. These pathways are encoded
    in a directed rooted graph in which the nodes represent the tipping points, and the edges
    the period of time an action is active.

    The information in this graph is very similar to the information in a pathways graph,
    but for the sake of visualizing a pathways map, additional nodes are added to the graph.
    """
