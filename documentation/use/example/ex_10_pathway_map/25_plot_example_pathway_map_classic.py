"""
Pathway map for an example
==========================
"""
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import (
    PathwayMapLayout,
    plot_pathway_map,
    read_sequences,
    read_tipping_points,
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
tipping_points = read_tipping_points(
    StringIO(
        """
current 2030
a 2100
b1 2040
c 2050
d 2100
b2 2070
"""
    ),
    pathway_map.actions(),
)

pathway_map.assign_tipping_points(tipping_points)

plot_pathway_map(pathway_map, layout=PathwayMapLayout.CLASSIC)
plt.show()
