"""
Pathway map for diverging pathways
==================================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import read_sequences, sequence_graph_to_pathway_map
from adaptation_pathways.plot import plot_default_pathway_map as plot


sequence_graph, _ = read_sequences(
    StringIO(
        """
current a
current b
current c
"""
    )
)
pathway_map = sequence_graph_to_pathway_map(sequence_graph)

plot(pathway_map)
plt.show()
