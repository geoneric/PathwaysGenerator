"""
Pathway graph for converging pathways
=====================================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import (
    read_sequence_graph,
    sequence_graph_to_pathway_graph,
)
from adaptation_pathways.plot import init_axes
from adaptation_pathways.plot import plot_default_pathway_graph as plot


sequence_graph = read_sequence_graph(
    StringIO(
        """
current a
current b
current c
a d
b d
c d
"""
    )
)
pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)

_, axes = plt.subplots(layout="constrained")
init_axes(axes)
plot(axes, pathway_graph)
plt.show()
