"""
Pathway graph for an example
============================
"""
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import (
    plot_pathway_graph,
    read_sequences,
    sequence_graph_to_pathway_graph,
)


sequence_graph, _ = read_sequences(
    StringIO(
        """
current a
a e
current b
b f
current c
c f
current d
d f
f e
"""
    )
)
pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)

plot_pathway_graph(pathway_graph)
plt.show()
