from .directed_graph import DirectedGraph


class RootedGraph(DirectedGraph):
    """
    Class for directed out-graphs in which each node can be reached from the one root node.
    """

    @property
    def root_node(self):
        """
        :return: The root node
        """

        root_nodes = [node for node, degree in self._graph.in_degree() if degree == 0]

        nr_root_nodes = len(root_nodes)

        if nr_root_nodes == 0:
            raise LookupError("Graph is empty")

        if nr_root_nodes > 1:
            raise LookupError(
                "Only single rooted graphs are supported, "
                f"but this graph contains {nr_root_nodes} root nodes"
            )

        return root_nodes[0]
