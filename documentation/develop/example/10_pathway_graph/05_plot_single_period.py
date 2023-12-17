"""
Pathway graph for single period
===============================
The simplest pathway is defined by the period between two actions. Given two actions (current
policy and action "a"), the pathway graph contains three nodes: the ``current`` Action, the
``current|a`` ActionConversion, and the ``a`` Action. The edges between them represent the
amount of time between the conversions.
"""
from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import (
    plot_pathway_graph,
    read_sequences,
    sequence_graph_to_pathway_graph,
)


sequence_graph = read_sequences(
    StringIO(
        """
current a
"""
    )
)
pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)

plot_pathway_graph(pathway_graph)
plt.show()
