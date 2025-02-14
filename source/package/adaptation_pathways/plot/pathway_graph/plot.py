import matplotlib as mpl

from ...graph import PathwayGraph
from .default import plot as plot_default


def plot_pathway_graph(
    axes: mpl.axes.Axes,
    pathway_graph: PathwayGraph,
    **arguments,
) -> None:
    """
    Plot a pathway graph

    Currently, this function plots using the default layout.

    See also: :func:`default.plot <adaptation_pathways.plot.pathway_graph.default.plot>`
    """
    plot_default(axes, pathway_graph, **arguments)
