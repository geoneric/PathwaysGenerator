from ...graph.pathway_graph import PathwayGraph
from ..colour import PlotColours
from .default import plot as plot_default


def plot_pathway_graph(
    pathway_graph: PathwayGraph,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    plot_default(pathway_graph, title, plot_colours)
