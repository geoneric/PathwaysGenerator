from ...graph.colour import PlotColours
from ...graph.pathway_map import PathwayMap
from ...graph.plot import PathwayMapLayout
from .classic import plot as plot_classic
from .default import plot as plot_default


def plot_pathway_map(
    pathway_map: PathwayMap,
    title: str = "",
    layout: PathwayMapLayout = PathwayMapLayout.DEFAULT,
    plot_colours: PlotColours | None = None,
) -> None:
    if layout == PathwayMapLayout.CLASSIC:
        plot_classic(pathway_map, title, plot_colours)
    else:
        plot_default(pathway_map, title, plot_colours)
