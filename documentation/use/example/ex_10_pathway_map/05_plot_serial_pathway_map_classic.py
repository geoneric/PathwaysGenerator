"""
Pathway map for serial sequence
===============================
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


sequence_graph, level_by_action = read_sequences(
    StringIO(
        """
current a
a b
b c
"""
    )
)
pathway_map = sequence_graph_to_pathway_map(sequence_graph)
tipping_points = read_tipping_points(
    StringIO(
        """
current 2030
a 2040
b 2050
c 2060
"""
    ),
    pathway_map.actions(),
)

pathway_map.assign_tipping_points(tipping_points)
pathway_map.set_attribute("level", level_by_action)

plot_pathway_map(pathway_map, layout=PathwayMapLayout.CLASSIC)
plt.tight_layout()
plt.show()
