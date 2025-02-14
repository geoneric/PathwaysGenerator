from .directed_graph import DirectedGraph


class MultiRootedGraph(DirectedGraph):
    """
    Class for directed out-graphs in which there can be multiple graphs rooted at independent nodes.
    """

    @property
    def root_nodes(self):
        """
        :return: The root nodes
        """

        return [node for node, degree in self._graph.in_degree() if degree == 0]
