import matplotlib.pyplot as plt

from ..graph.colour import PlotColours, default_pathway_map_colours
from ..graph.layout.pathway_map import classic_layout as classic_pathway_map_layout
from ..graph.layout.pathway_map import default_layout as default_pathway_map_layout
from ..graph.pathway_map import PathwayMap
from ..graph.plot import PathwayMapLayout, init_plot, save_plot


# pylint: skip-file
# flake8: noqa


def plot_default_pathway_map(
    pathway_map: PathwayMap,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    if plot_colours is None:
        plot_colours = default_pathway_map_colours(pathway_map)

    init_plot(
        pathway_map.graph,
        title,
        default_pathway_map_layout(pathway_map),
        plot_colours,
    )


def classic_pathway_map_plotter(
    axes,
    pathway_map,
    layout,
    title,
    plot_colours,
) -> None:
    # TODO
    # - Get rid of the frames
    # - Draw edges
    # - Draw nodes
    # - Add action labels
    # - Support dashed lines when multiple colours are passed for an edge
    # - Can we add multiple x-axis on top of each other?
    #     - https://pythonmatplotlibtips.blogspot.com/2018/01/add-second-x-axis-below-first-x-axis-python-matplotlib-pyplot.html
    #     - https://matthewkudija.com/blog/2019/02/13/matplotlib-twin-axes/
    # - Understand size and scale of plot + coordinates

    # Once we understand plotting with matplotlib, adjust the layout of parallel pathways. They
    # need to be separated a bit vertically.
    # - Use existing distribute function, center around Action's y-coordinate

    # edge_artist = edge_plotter(...)
    # node_artist = node_plotter(...)

    axes.set_xlabel("x label TODO")
    axes.set_ylabel("y label TODO")

    if len(title) > 0:
        axes.set_title(title)

    # Return the result(s) of a plot function(s) (artists?)
    # return edge_artist, node_artist


def plot_classic_pathway_map(
    pathway_map: PathwayMap,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    layout = classic_pathway_map_layout(pathway_map)

    if plot_colours is None:
        plot_colours = default_pathway_map_colours(pathway_map)

    # https://matplotlib.org/stable/users/explain/figure/api_interfaces.html#api-interfaces
    figure, axes = plt.subplots(figsize=(5, 2.7), layout="constrained")

    classic_pathway_map_plotter(axes, pathway_map, layout, title, plot_colours)


def plot_pathway_map(
    pathway_map: PathwayMap,
    title: str = "",
    layout: PathwayMapLayout = PathwayMapLayout.DEFAULT,
    plot_colours: PlotColours | None = None,
) -> None:
    if layout == PathwayMapLayout.CLASSIC:
        plot_classic_pathway_map(pathway_map, title, plot_colours)
    else:
        plot_default_pathway_map(pathway_map, title, plot_colours)


def plot_and_save_pathway_map(
    pathway_map: PathwayMap,
    pathname: str,
    title: str = "",
    layout: PathwayMapLayout = PathwayMapLayout.DEFAULT,
    plot_colours: PlotColours | None = None,
) -> None:
    plot_pathway_map(
        pathway_map,
        title,
        layout,
        plot_colours,
    )
    save_plot(pathname)
