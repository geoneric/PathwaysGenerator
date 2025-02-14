import os.path
import sys
import typing

import docopt
import matplotlib.pyplot as plt

import adaptation_pathways as ap

from ..graph import PathwayGraph, PathwayMap, SequenceGraph
from ..io import read_dataset
from ..plot.pathway_graph import plot_default_pathway_graph
from ..plot.pathway_map import plot_default_pathway_map
from ..plot.sequence_graph import plot_default_sequence_graph
from ..plot.util import init_axes, save_plot
from .main import main_function


def plot_sequence_graph(graph: SequenceGraph, axes, arguments, pathname):
    axes.clear()
    plot_default_sequence_graph(axes, graph, **arguments)
    save_plot(pathname)


def plot_pathway_graph(graph: PathwayGraph, axes, arguments, pathname):
    axes.clear()
    plot_default_pathway_graph(axes, graph, **arguments)
    save_plot(pathname)


def plot_pathway_map(graph: PathwayMap, axes, arguments, pathname):
    axes.clear()
    plot_default_pathway_map(axes, graph, **arguments)
    save_plot(pathname)


@main_function
def plot_graphs(
    basename_pathname: str, plots_prefix_pathname: str, output_format: str
) -> int:

    # pylint: disable-next=unused-variable
    actions, sequences, tipping_point_by_action, colour_by_action = read_dataset(
        basename_pathname
    )

    colour_by_action_name = {
        action.name: colour for action, colour in colour_by_action.items()
    }

    _, axes = plt.subplots(layout="constrained")
    init_axes(axes)

    basename = os.path.splitext(os.path.basename(basename_pathname))[0]
    assert os.path.isdir(plots_prefix_pathname), plots_prefix_pathname

    arguments: dict[str, typing.Any] = {
        "colour_by_action_name": colour_by_action_name,
    }

    sequence_graph = SequenceGraph(sequences)
    plot_pathname = os.path.join(
        plots_prefix_pathname, f"{basename}-sequence_graph.{output_format}"
    )
    arguments["title"] = "Sequence graph"
    plot_sequence_graph(sequence_graph, axes, arguments, plot_pathname)

    pathway_graph = ap.graph.sequence_graph_to_pathway_graph(sequence_graph)
    plot_pathname = os.path.join(
        plots_prefix_pathname, f"{basename}-pathway_graph.{output_format}"
    )
    arguments["title"] = "Pathway graph"
    plot_pathway_graph(pathway_graph, axes, arguments, plot_pathname)

    pathway_map = ap.graph.pathway_graph_to_pathway_map(pathway_graph)
    plot_pathname = os.path.join(
        plots_prefix_pathname, f"{basename}-pathway_map.{output_format}"
    )
    arguments["title"] = "Pathway map"
    plot_pathway_map(pathway_map, axes, arguments, plot_pathname)

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Plot sequence and pathway graphs

Usage:
    {command} [--format=<format>] <basename> <prefix>

Arguments:
    basename           Either, the name without postfix and extension of text
                       file(s) to read information from, or the name of a
                       binary file to read information from.
    prefix             Name of directory to store plots in. The file name will
                       be based on the basename passed in and the kind of plot
                       in the file.

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit
    --format=<format>  Output format for plots [default: pdf]

Example:
    {command} serial .
    {command} serial.apw .
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=ap.__version__)
    basename_pathname = arguments["<basename>"]  # type: ignore
    plots_prefix_pathname = arguments["<prefix>"]  # type: ignore
    output_format = arguments["--format"]  # type: ignore

    return plot_graphs(basename_pathname, plots_prefix_pathname, output_format)
