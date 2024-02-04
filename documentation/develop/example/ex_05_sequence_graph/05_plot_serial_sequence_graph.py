"""
Sequence graph for serial sequence
==================================
"""
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import plot_sequence_graph, read_sequences


sequence_graph, _ = read_sequences(
    StringIO(
        """
current a
a b
b c
"""
    )
)

plot_sequence_graph(sequence_graph)
plt.show()
