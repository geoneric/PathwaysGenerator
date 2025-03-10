"""
Sequence graph for serial sequence
==================================
"""

import typing
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import SequenceGraph
from adaptation_pathways.io import text
from adaptation_pathways.plot.sequence_graph import plot_default_sequence_graph
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
current[1] current
current a
a b
b c
"""
    ),
    actions,
)
sequence_graph = SequenceGraph(sequences)

arguments: dict[str, typing.Any] = {
    "colour_by_action_name": colour_by_action_name,
}

_, axes = plt.subplots(layout="constrained")
init_axes(axes)
plot_default_sequence_graph(axes, sequence_graph, **arguments)
plt.show()
