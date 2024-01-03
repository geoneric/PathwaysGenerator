"""
Pathway map for an example
==========================
"""
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import (
    plot_pathway_map,
    read_sequences,
    sequence_graph_to_pathway_map,
)


sequence_graph = read_sequences(
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
pathway_map = sequence_graph_to_pathway_map(sequence_graph)

plot_pathway_map(pathway_map)
plt.show()
