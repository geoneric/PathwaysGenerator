import enum
import typing

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from .colour import (
    PlotColours,
    default_pathway_graph_colours,
    default_pathway_map_colours,
    default_sequence_graph_colours,
)
from .layout.pathway_graph import default_layout as pathway_graph_layout
from .layout.pathway_map import classic_layout as classic_pathway_map_layout
from .layout.pathway_map import default_layout as default_pathway_map_layout
from .layout.sequence_graph import default_layout as sequence_graph_layout
from .pathway_graph import PathwayGraph
from .pathway_map import PathwayMap
from .sequence_graph import SequenceGraph


PathwayMapLayout = enum.Enum("PathwayMapLayout", ["DEFAULT", "CLASSIC"])


def init_plot(
    graph: nx.DiGraph,
    title: str,
    layout: dict[typing.Any, np.ndarray],
    plot_colours: PlotColours,
) -> None:
    plt.rc(
        "axes.spines", **{"bottom": False, "left": False, "right": False, "top": False}
    )

    # draw_options = {
    #     "with_labels": True,
    #     "font_size": "small",
    #     "font_weight": "bold",
    # }

    _, axis = plt.subplots()

    title = title.strip()

    if len(title) > 0:
        axis.set_title(title)

    # nx.draw_networkx(
    #     graph, pos=layout, node_color=node_colours, edge_color=edge_colours, **draw_options
    # )

    nx.draw_networkx_edges(
        graph,
        pos=layout,
        edge_color=plot_colours.edge_colours,
        width=1.0,
        arrows=False,
        # style="dashed",
    )

    nx.draw_networkx_nodes(
        graph,
        pos=layout,
        node_color=plot_colours.node_colours,
        node_size=250,
        linewidths=0.5,
        edgecolors=plot_colours.node_edge_colours,
    )

    nx.draw_networkx_labels(
        graph,
        pos=layout,
        font_size="medium",
        font_weight="bold",
        verticalalignment="bottom",
        horizontalalignment="right",
        font_color=plot_colours.label_colour,
    )


def save_plot(pathname: str) -> None:
    plt_options = {
        "bbox_inches": "tight",
        "transparent": True,
    }
    plt.savefig(pathname, **plt_options)


def plot_sequence_graph(
    sequence_graph: SequenceGraph,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    if plot_colours is None:
        plot_colours = default_sequence_graph_colours(sequence_graph)

    init_plot(
        sequence_graph.graph,
        title,
        sequence_graph_layout(sequence_graph),
        plot_colours,
    )


def plot_and_save_sequence_graph(
    sequence_graph: SequenceGraph,
    pathname: str,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    plot_sequence_graph(
        sequence_graph,
        title,
        plot_colours,
    )
    save_plot(pathname)


def plot_pathway_graph(
    pathway_graph: PathwayGraph,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    if plot_colours is None:
        plot_colours = default_pathway_graph_colours(pathway_graph)

    init_plot(
        pathway_graph.graph,
        title,
        pathway_graph_layout(pathway_graph),
        plot_colours,
    )


def plot_and_save_pathway_graph(
    pathway_graph: PathwayGraph,
    pathname: str,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    plot_pathway_graph(
        pathway_graph,
        title,
        plot_colours,
    )
    save_plot(pathname)


def plot_pathway_map(
    pathway_map: PathwayMap,
    title: str = "",
    layout: PathwayMapLayout = PathwayMapLayout.DEFAULT,
    plot_colours: PlotColours | None = None,
) -> None:
    if layout == PathwayMapLayout.CLASSIC:
        pathway_map_layout = classic_pathway_map_layout
    else:
        pathway_map_layout = default_pathway_map_layout

    if plot_colours is None:
        plot_colours = default_pathway_map_colours(pathway_map)

    init_plot(
        pathway_map.graph,
        title,
        pathway_map_layout(pathway_map),
        plot_colours,
    )


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
