"""
Pathway map for serial sequence
===============================
"""
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import (
    plot_pathway_map,
    read_sequences,
    sequence_graph_to_pathway_map,
)


sequence_graph, _ = read_sequences(
    StringIO(
        """
current a
a b
b c
"""
    )
)
pathway_map = sequence_graph_to_pathway_map(sequence_graph)
plot_pathway_map(pathway_map)
plt.show()
