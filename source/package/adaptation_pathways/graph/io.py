import io

import networkx as nx

from ..action import Action
from .sequence_graph import SequenceGraph


def read_sequences(sequences_pathname: str | io.IOBase) -> SequenceGraph:
    graph = nx.read_edgelist(sequences_pathname, create_using=nx.DiGraph)
    actions = {action_label: Action(action_label) for action_label in graph.nodes()}
    sequence_graph = SequenceGraph()

    for from_action_label, to_action_label in graph.edges():
        sequence_graph.add_sequence(
            actions[from_action_label], actions[to_action_label]
        )

    return sequence_graph
