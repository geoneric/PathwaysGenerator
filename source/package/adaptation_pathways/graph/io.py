import io

import networkx as nx

from .node import Action
from .sequence_graph import SequenceGraph


def read_tipping_points(
    tipping_points_pathname: str | io.IOBase, actions: list[Action]
) -> dict[Action, int]:
    tipping_points_file: io.IOBase

    if isinstance(tipping_points_pathname, str):
        tipping_points_file = open(tipping_points_pathname, encoding="utf-8")
    else:
        tipping_points_file = tipping_points_pathname

    tipping_point_by_label: dict[str, int] = {}

    with tipping_points_file:
        for line in tipping_points_file:
            line_as_string = str(line.strip())  # Keep mypy happy

            if len(line_as_string) > 0 and not line_as_string.startswith("#"):
                label, tipping_point_as_string = line_as_string.strip().split()
                tipping_point = int(tipping_point_as_string)  # Keep mypy happy
                tipping_point_by_label[label] = int(tipping_point)

    tipping_point_by_action: dict[Action, int] = {}

    # Multiple actions can have the same label. Assign the same tipping point to all of them.
    for label, tipping_point in tipping_point_by_label.items():
        for action in actions:
            if action.label == label:
                tipping_point_by_action[action] = tipping_point

    return tipping_point_by_action


def read_sequences(sequences_pathname: str | io.IOBase) -> SequenceGraph:
    graph = nx.read_edgelist(sequences_pathname, create_using=nx.DiGraph)
    actions = {action_label: Action(action_label) for action_label in graph.nodes()}
    sequence_graph = SequenceGraph()

    for from_action_label, to_action_label in graph.edges():
        sequence_graph.add_sequence(
            actions[from_action_label], actions[to_action_label]
        )

    return sequence_graph
