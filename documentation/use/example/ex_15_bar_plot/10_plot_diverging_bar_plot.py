"""
Bar plot for diverging pathways
===============================
"""

import typing
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import SequenceGraph, sequence_graph_to_pathway_map
from adaptation_pathways.io import text
from adaptation_pathways.plot.bar_plot import plot_bars
from adaptation_pathways.plot.util import init_axes


actions, colour_by_action_name = text.read_actions(
    StringIO(
        """
current #ff4c566a
a #ffbf616a
b #ffd08770
c #ffebcb8b
"""
    )
)
sequences, tipping_point_by_action = text.read_sequences(
    StringIO(
        """
current current 2030
current a 2040
current b 2050
current c 2060
"""
    ),
    actions,
)
sequence_graph = SequenceGraph(sequences)
pathway_map = sequence_graph_to_pathway_map(sequence_graph)

arguments: dict[str, typing.Any] = {
    "colour_by_action_name": colour_by_action_name,
    "tipping_point_by_action": tipping_point_by_action,
}

_, axes = plt.subplots(layout="constrained")
init_axes(axes)
plot_bars(axes, pathway_map, **arguments)
plt.show()
