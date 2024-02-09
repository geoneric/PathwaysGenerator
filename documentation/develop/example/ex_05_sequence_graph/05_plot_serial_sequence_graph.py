"""
Sequence graph for serial sequence
==================================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import read_sequences
from adaptation_pathways.plot import plot_default_sequence_graph as plot


sequence_graph, _ = read_sequences(
    StringIO(
        """
current a
a b
b c
"""
    )
)

plot(sequence_graph)
plt.show()
