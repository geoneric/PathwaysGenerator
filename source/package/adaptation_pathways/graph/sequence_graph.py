import networkx as nx

from ..action import Action
from .rooted_graph import RootedGraph


class SequenceGraph(RootedGraph):
    """
    A SequenceGraph represents the dependencies between actions. Each node represents an action,
    and each edge the fact that one action follows another one.
    """

    def add_action(self, action: Action) -> None:
        """
        Add an action

        :param action: Action
        """
        self._graph.add_node(action)

    def add_sequence(self, from_action: Action, to_action: Action) -> None:
        """
        Add a sequence of actions

        :param from_action: First action of the sequence
        :param to_action: Second action of the sequence
        """
        self._graph.add_edge(from_action, to_action)

    def add_sequences(self, actions: list[tuple[Action, Action]]) -> None:
        """
        Add sequences of actions

        :param actions: List of tuples of ``from_action`` and ``to_action``
        """
        return self._graph.add_edges_from(actions)

    def nr_actions(self) -> int:
        """
        :return: Number of actions
        """
        return self.nr_nodes()

    def nr_from_actions(self, to_action: Action) -> int:
        """
        :return: Number of sequences that end at the action passed in

        In graph-speek, this is the action's in-degree.
        """
        return self._graph.in_degree(to_action)

    def from_actions(self, to_action: Action) -> list[Action]:
        """
        :return: Collection of actions that end at the action passed in
        """
        # TODO Can this be done more efficiently?
        return [
            action
            for action in self._graph.nodes()
            if to_action in self.to_actions(action)
        ]

    def nr_to_actions(self, from_action: Action) -> int:
        """
        :return: Number of sequences that start at the action passed in

        In graph-speek, this is the action's out-degree.
        """
        return self._graph.out_degree(from_action)

    def to_actions(self, from_action: Action) -> list[Action]:
        """
        :return: Collection of actions that start at the action passed in
        """
        return list(self._graph.adj[from_action])

    def nr_sequences(self) -> int:
        """
        :return: Number of sequences
        """
        return len(self._graph.edges)

    def all_to_actions(self, from_action: Action) -> list[Action]:
        # Use shortest_path to find all actions reachable from the action passed in
        graph = self._graph.subgraph(nx.shortest_path(self._graph, from_action))

        # Remove the from_action itself before returning the result
        return list(graph.nodes)[1:]
