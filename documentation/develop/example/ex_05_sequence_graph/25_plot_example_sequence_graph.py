"""
Sequence graph for an example
=============================
This example is taken from the adaptation pathways documentation.

The same action ``b`` is used in different pathways. Therefore, in the specification of the
sequences, ``b1`` and ``b2`` are used, even though these two are the same action.
"""
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import plot_sequence_graph, read_sequences


sequence_graph, _ = read_sequences(
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

plot_sequence_graph(sequence_graph)
plt.show()
