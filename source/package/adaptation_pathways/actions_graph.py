import networkx as nx

from .action import Action


class ActionsGraph:
    _graph: nx.DiGraph

    def __init__(self) -> None:
        self._graph = nx.DiGraph()

    @property
    def graph(self) -> nx.DiGraph:
        return self._graph

    def add_action(self, action: Action) -> None:
        self._graph.add_node(action)

    def add_sequence(self, from_action: Action, to_action: Action) -> None:
        self._graph.add_edge(from_action, to_action)

    def add_sequences(self, actions: list[tuple[Action, Action]]) -> None:
        return self._graph.add_edges_from(actions)
