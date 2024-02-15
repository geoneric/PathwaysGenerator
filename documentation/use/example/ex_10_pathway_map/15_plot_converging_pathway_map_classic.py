"""
Pathway map for converging pathways
===================================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import (
    action_level_by_first_occurrence,
    read_sequences,
    read_tipping_points,
    sequence_graph_to_pathway_map,
    sequences_to_sequence_graph,
)
from adaptation_pathways.plot import plot_classic_pathway_map as plot


sequences = read_sequences(
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
sequence_graph = sequences_to_sequence_graph(sequences)
level_by_action = action_level_by_first_occurrence(sequences)

pathway_map = sequence_graph_to_pathway_map(sequence_graph)
tipping_points = read_tipping_points(
    StringIO(
        """
current 2030
a 2040
b 2050
c 2060
d 2070
"""
    ),
    pathway_map.actions(),
)

pathway_map.assign_tipping_points(tipping_points)
pathway_map.set_attribute("level", level_by_action)

plot(pathway_map)
plt.show()
