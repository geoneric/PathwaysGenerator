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

        Try not to use it -- it should be an implementation detail as much as possible.
        """
        return self._graph

    # def is_empty(self) -> bool:
    #     """
    #     :return: Wheter or not the tree is empty
    #     """
    #     return nx.is_empty(self._graph)

    def nr_nodes(self) -> int:
        """
        :return: Number of nodes
        """
        return len(self._graph.nodes)

    def nr_edges(self) -> int:
        """
        :return: Number of edges
        """
        return len(self._graph.edges)

    @property
    def root_node(self):
        """
        :return: The root node
        """
        return next(nx.topological_sort(self._graph))
        # print(self._graph.in_degree())
        # print([node for node, degree in self._graph.in_degree()])
        # return [node for node, degree in self._graph.in_degree() if degree == 0][0]
