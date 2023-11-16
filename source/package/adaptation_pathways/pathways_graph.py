import networkx as nx

from .action import Action
from .sequenced_action import SequencedAction


class PathwaysGraph:
    _graph: nx.DiGraph

    def __init__(self) -> None:
        self._graph = nx.DiGraph()

    @property
    def graph(self) -> nx.DiGraph:
        return self._graph

    def add_action(self, from_action: Action, to_action: Action) -> None:
        # Think "horizontal line in pathways map"
        self._graph.add_edge(from_action, to_action)

    def add_sequence(self, action: SequencedAction) -> None:
        # Think "vertical line in pathways map"
        self._graph.add_node(action)
