"""
Sequence graph for an example
=============================
Note that ``e`` has in-degree of two, ``f`` has in-degree of three, but since ``e`` follows
``f``, ``e`` it must be positioned to the right of ``f``.
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import read_sequence_graph
from adaptation_pathways.plot import plot_default_sequence_graph as plot


sequence_graph = read_sequence_graph(
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

plot(sequence_graph)
plt.show()
