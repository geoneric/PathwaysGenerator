import networkx as nx


class RootedGraph:
    """
    A rooted graph represents a directed out-graph in which each node can be reached from the
    root node.
    """

    _graph: nx.DiGraph

    def __init__(self) -> None:
        self._graph = nx.DiGraph()

    def __str__(self) -> str:
        return "\n".join(nx.generate_network_text(self._graph))

    @property
    def graph(self) -> nx.DiGraph:
        """
        :return: The layered directed graph instance
        """
        return self._graph

    @property
    def is_empty(self) -> bool:
        """
        :return: Wheter or not the tree is empty
        """
        return nx.is_empty(self._graph)

    @property
    def root_node(self):
        """
        :return: The root node
        """
        return next(nx.topological_sort(self._graph))
        # print(self._graph.in_degree())
        # print([node for node, degree in self._graph.in_degree()])
        # return [node for node, degree in self._graph.in_degree() if degree == 0][0]
