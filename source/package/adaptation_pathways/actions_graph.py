from .action import Action
from .rooted_graph import RootedGraph


class ActionsGraph(RootedGraph):
    """
    An ActionsGraph represents the dependencies between actions. The nodes represent the actions,
    and the edges the fact that actions follow each other in ѕequences.
    """

    def add_sequence(self, from_action: Action, to_action: Action) -> None:
        """
        Add a sequence of actions

        :param from_action: First action of the sequence
        :param to_action: Second action of the sequence
        """
        self._graph.add_edge(from_action, to_action)

    def add_sequences(self, actions: list[tuple[Action, Action]]) -> None:
        """
        Add a sequences of actions

        :param actions: List of tuples of ``from_action`` and ``to_action``
        """
        return self._graph.add_edges_from(actions)
