"""
Pathway graph for converging pathways
=====================================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import conversion
from adaptation_pathways.io import text
from adaptation_pathways.plot import init_axes
from adaptation_pathways.plot import plot_default_pathway_graph as plot


actions, colour_by_action = text.read_actions(
    StringIO(
        """
current
a
b
c
d
"""
    )
)
sequences, tipping_point_by_action = text.read_sequences(
    StringIO(
        """
current[1] current
current a
current b
current c
a d[1]
b d[2]
c d[3]
"""
    )
)
sequence_graph = conversion.sequences_to_sequence_graph(sequences)
pathway_graph = conversion.sequence_graph_to_pathway_graph(sequence_graph)

_, axes = plt.subplots(layout="constrained")
init_axes(axes)
plot(axes, pathway_graph)
plt.show()
