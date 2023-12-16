"""
Sequence graph for diverging sequence
=====================================
"""
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import plot_sequence_graph, read_sequences


graph = read_sequences(
    StringIO(
        """
current a
current b
current c
"""
    )
)


plot_sequence_graph(graph)
plt.show()
