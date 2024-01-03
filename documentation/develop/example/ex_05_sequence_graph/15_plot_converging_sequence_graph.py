"""
Sequence graph for converging sequence
======================================
"""
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import plot_sequence_graph, read_sequences


sequence_graph = read_sequences(
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


plot_sequence_graph(sequence_graph)
plt.show()
