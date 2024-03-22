import os.path
import sys

import docopt
import matplotlib.pyplot as plt

import adaptation_pathways as ap

from .. import alias
from ..graph import PathwayGraph, PathwayMap, SequenceGraph, sequences_to_sequence_graph
from ..io import sqlite, text
from ..plot import (
    init_axes,
    pathway_graph_node_colours,
    pathway_map_edge_colours,
    pathway_map_node_colours,
    plot_default_pathway_graph,
    plot_default_pathway_map,
    plot_default_sequence_graph,
    save_plot,
    sequence_graph_node_colours,
)
from ..plot.colour import (
    PlotColours,
    default_edge_colours,
    default_label_colour,
    default_node_edge_colours,
)
from .main import main_function


def plot_sequence_graph(
    graph: SequenceGraph,
    colour_by_action_name: alias.ColourByActionName,
    axes,
    pathname,
):
    plot_colours = PlotColours(
        sequence_graph_node_colours(graph, colour_by_action_name),
        default_edge_colours(graph),
        default_node_edge_colours(graph),
        default_label_colour(),
    )

    axes.clear()
    plot_default_sequence_graph(
        axes, graph, title="Sequence graph", plot_colours=plot_colours
    )
    save_plot(pathname)


def plot_pathway_graph(
    graph: PathwayGraph, colour_by_action_name: alias.ColourByActionName, axes, pathname
):
    plot_colours = PlotColours(
        pathway_graph_node_colours(graph, colour_by_action_name),
        default_edge_colours(graph),
        default_node_edge_colours(graph),
        default_label_colour(),
    )

    axes.clear()
    plot_default_pathway_graph(
        axes, graph, title="Pathway graph", plot_colours=plot_colours
    )
    save_plot(pathname)


def plot_pathway_map(
    graph: PathwayMap, colour_by_action_name: alias.ColourByActionName, axes, pathname
):
    plot_colours = PlotColours(
        pathway_map_node_colours(graph, colour_by_action_name),
        pathway_map_edge_colours(graph, colour_by_action_name),
        default_node_edge_colours(graph),
        default_label_colour(),
    )

    axes.clear()
    plot_default_pathway_map(
        axes, graph, title="Pathway map", plot_colours=plot_colours
    )
    save_plot(pathname)


@main_function
def plot_graphs(
    basename_pathname: str, plots_prefix_pathname: str, output_format: str
) -> int:

    if sqlite.dataset_exists(basename_pathname):
        # pylint: disable-next=unused-variable
        actions, sequences, tipping_point_by_action, colour_by_action = (
            sqlite.read_dataset(basename_pathname)
        )
    else:
        # pylint: disable-next=unused-variable
        actions, sequences, typping_point_by_action, colour_by_action = (
            text.read_dataset(basename_pathname)
        )

    colour_by_action_name = {
        action.name: colour for action, colour in colour_by_action.items()
    }

    _, axes = plt.subplots(layout="constrained")
    init_axes(axes)

    basename = os.path.splitext(os.path.basename(basename_pathname))[0]
    assert os.path.isdir(plots_prefix_pathname), plots_prefix_pathname

    sequence_graph = sequences_to_sequence_graph(sequences)
    plot_pathname = os.path.join(
        plots_prefix_pathname, f"{basename}-sequence_graph.{output_format}"
    )
    plot_sequence_graph(sequence_graph, colour_by_action_name, axes, plot_pathname)

    pathway_graph = ap.graph.sequence_graph_to_pathway_graph(sequence_graph)
    plot_pathname = os.path.join(
        plots_prefix_pathname, f"{basename}-pathway_graph.{output_format}"
    )
    plot_pathway_graph(pathway_graph, colour_by_action_name, axes, plot_pathname)

    pathway_map = ap.graph.pathway_graph_to_pathway_map(pathway_graph)
    plot_pathname = os.path.join(
        plots_prefix_pathname, f"{basename}-pathway_map.{output_format}"
    )
    plot_pathway_map(pathway_map, colour_by_action_name, axes, plot_pathname)

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Plot sequence and pathway graphs

Usage:
    {command} [--format=<format>] <basename> <prefix>

Arguments:
    basename           Name, without postfix and extension of group of file(s)
                       to read information from. This can be a set of text files
                       or a single binary file.
    prefix             Name of directory to store plots in. The file name will
                       be based on the basename passed in and the kind of plot
                       in the file.

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit
    --format=<format>  Output format for plots [default: pdf]

Example:
    {command} serial .
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=ap.__version__)
    basename_pathname = arguments["<basename>"]  # type: ignore
    plots_prefix_pathname = arguments["<prefix>"]  # type: ignore
    output_format = arguments["--format"]  # type: ignore

    return plot_graphs(basename_pathname, plots_prefix_pathname, output_format)
