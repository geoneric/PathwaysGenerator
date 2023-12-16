"""
Sequence graph for example 01
=============================
Note that ``e`` has in-degree of two, ``f`` has in-degree of three, but since ``e`` follows
``f``, ``e`` it must be positioned to the right of ``f``.
"""
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import plot_sequence_graph, read_sequences


graph = read_sequences(
    StringIO(
        """
current a
a e
current b
b f
current c
c f
current d
d f
f e
"""
    )
)

plot_sequence_graph(graph)
plt.show()
