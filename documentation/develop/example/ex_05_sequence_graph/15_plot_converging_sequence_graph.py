"""
Sequence graph for converging sequence
======================================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import read_sequence_graph
from adaptation_pathways.plot import plot_default_sequence_graph as plot


sequence_graph = read_sequence_graph(
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


plot(sequence_graph)
plt.show()
