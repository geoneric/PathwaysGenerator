import networkx as nx


class RootedTree:
    """
    A rooted tree represents a directed graph in which each node can reach the same root node.
    """

    _graph: nx.DiGraph

    def __init__(self) -> None:
        self._graph = nx.DiGraph()

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
