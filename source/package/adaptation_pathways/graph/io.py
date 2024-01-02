import io

import networkx as nx

from .node import Action
from .sequence_graph import SequenceGraph


def read_tipping_points(tipping_points_pathname: str | io.IOBase) -> dict[str, int]:
    tipping_points: dict[str, int] = {}

    tipping_points_file: io.IOBase

    if isinstance(tipping_points_pathname, str):
        tipping_points_file = open(tipping_points_pathname, encoding="utf-8")
    else:
        tipping_points_file = tipping_points_pathname

    with tipping_points_file:
        for line in tipping_points_file:
            label, tipping_point = line.strip().split()
            tipping_points[str(label)] = int(tipping_point)

    return tipping_points


def read_sequences(sequences_pathname: str | io.IOBase) -> SequenceGraph:
    graph = nx.read_edgelist(sequences_pathname, create_using=nx.DiGraph)
    actions = {action_label: Action(action_label) for action_label in graph.nodes()}
    sequence_graph = SequenceGraph()

    for from_action_label, to_action_label in graph.edges():
        sequence_graph.add_sequence(
            actions[from_action_label], actions[to_action_label]
        )

    return sequence_graph
