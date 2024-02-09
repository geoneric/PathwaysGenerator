"""
Pathway graph for serial pathway
================================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import read_sequences, sequence_graph_to_pathway_graph
from adaptation_pathways.plot import plot_default_pathway_graph as plot


sequence_graph, _ = read_sequences(
    StringIO(
        """
current a
a b
b c
"""
    )
)
pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)

plot(pathway_graph)
plt.show()
