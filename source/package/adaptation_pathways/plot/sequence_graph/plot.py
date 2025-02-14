import matplotlib as mpl

from ...graph import SequenceGraph
from .default import plot as plot_default


def plot_sequence_graph(
    axes: mpl.axes.Axes,
    sequence_graph: SequenceGraph,
    **arguments,
) -> None:
    """
    Plot a sequence graph

    Currently, this function plots using the default layout.

    See also: :func:`default.plot <adaptation_pathways.plot.sequence_graph.default.plot>`
    """
    plot_default(axes, sequence_graph, **arguments)
