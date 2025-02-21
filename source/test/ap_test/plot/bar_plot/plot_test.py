import typing
import unittest
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import (
    PathwayMap,
    SequenceGraph,
    sequence_graph_to_pathway_map,
)
from adaptation_pathways.io.text import (
    read_actions,
    read_sequences,
)
from adaptation_pathways.plot.bar_plot import plot_bars


def configure_pathway_map(
    actions_str: str, sequences_str: str
) -> tuple[PathwayMap, dict[str, typing.Any]]:

    actions, _ = read_actions(StringIO(actions_str))

    sequences, tipping_point_by_action = read_sequences(
        StringIO(sequences_str), actions
    )

    sequence_graph = SequenceGraph(sequences)
    pathway_map = sequence_graph_to_pathway_map(sequence_graph)

    arguments = {
        "tipping_point_by_action": tipping_point_by_action,
    }

    return pathway_map, arguments


class PlotBarsTest(unittest.TestCase):

    def test_default_ordering(self):
        actions = """
            current
            a
            b
            c
            """
        sequences = """
            current current 2030
            current a 2040
            current b 2050
            current c 2060
            """
        pathway_map, arguments = configure_pathway_map(actions, sequences)
        arguments["label_by_pathway"] = {
            path[-1].action: path[-1].action.name for path in pathway_map.all_paths()
        }

        _, axes = plt.subplots(layout="constrained")

        plot_bars(axes, pathway_map, **arguments)

        labels, y_coordinates = zip(
            *[
                (label.get_text(), label.get_position()[1])
                for label in axes.get_yticklabels()
            ]
        )

        # NOTE: Y-axis coordinates are reversed by plot_bars. They increase top to bottom.
        self.assertSequenceEqual(labels, ["a", "b", "c"])
        self.assertSequenceEqual(y_coordinates, [0, 1, 2])

    def test_reverse_ordering(self):
        actions = """
            current
            a
            b
            c
            """
        sequences = """
            current current 2030
            current a 2040
            current b 2050
            current c 2060
            """
        pathway_map, arguments = configure_pathway_map(actions, sequences)
        arguments["label_by_pathway"] = {
            path[-1].action: path[-1].action.name for path in pathway_map.all_paths()
        }
        arguments["level_by_pathway"] = {
            path[-1].action: -idx for idx, path in enumerate(pathway_map.all_paths())
        }

        _, axes = plt.subplots(layout="constrained")

        plot_bars(axes, pathway_map, **arguments)

        labels, y_coordinates = zip(
            *[
                (label.get_text(), label.get_position()[1])
                for label in axes.get_yticklabels()
            ]
        )

        self.assertSequenceEqual(labels, ["c", "b", "a"])
        self.assertSequenceEqual(y_coordinates, [0, 1, 2])
