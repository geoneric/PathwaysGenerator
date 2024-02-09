"""
Pathway graph for an example
============================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import read_sequences, sequence_graph_to_pathway_graph
from adaptation_pathways.plot import plot_default_pathway_graph as plot


sequence_graph, _ = read_sequences(
    StringIO(
        """
current a
current b1
current c
current d
b1 a
b1 c
b1 d
c b2
b2 a
c a
c d
"""
    )
)
pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)

plot(pathway_graph)
plt.show()
