import os.path
import sys

import docopt

import adaptation_pathways as ap

from ..graph.io import read_sequences
from ..plot import (
    plot_default_pathway_graph,
    plot_default_pathway_map,
    plot_default_sequence_graph,
    save_plot,
)
from .main import main_function


@main_function
def plot_graphs(
    sequences_pathname: str, plots_prefix_pathname: str, output_format: str
) -> int:
    sequence_graph, _ = read_sequences(sequences_pathname)
    pathway_graph = ap.graph.sequence_graph_to_pathway_graph(sequence_graph)
    pathway_map = ap.graph.pathway_graph_to_pathway_map(pathway_graph)

    assert os.path.isdir(plots_prefix_pathname), plots_prefix_pathname

    basename = os.path.splitext(os.path.basename(sequences_pathname))[0]

    plot_pathname = os.path.join(
        plots_prefix_pathname, f"{basename}-sequence_graph.{output_format}"
    )
    plot_default_sequence_graph(sequence_graph, title="Sequence graph")
    save_plot(plot_pathname)

    plot_pathname = os.path.join(
        plots_prefix_pathname, f"{basename}-pathway_graph.{output_format}"
    )
    plot_default_pathway_graph(pathway_graph, title="Pathway graph")
    save_plot(plot_pathname)

    plot_pathname = os.path.join(
        plots_prefix_pathname, f"{basename}-pathway_map.{output_format}"
    )
    plot_default_pathway_map(pathway_map, title="Pathway map")
    save_plot(plot_pathname)

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Plot sequence and pathway graphs

Usage:
    {command} [--format=<format>] <sequences> <prefix>

Arguments:
    sequences          Name of file containing sequences of actions
    prefix             Name of directory to store plots in. The file name will
                       be based on the name of the sequences file passed in
                       and the kind of plot in the file.

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit
    --format=<format>  Output format for plots [default: pdf]

The format for storing sequences is simple: per line mention the names of
two actions that form a sequence. Information from multiple lines can result
in longer sequences. To allow for the same action to occur in different
sequences, a number can be added to the name.

Example:

current a
current b1
current c
current d
b1 a
b1 c
b1 d
c b2
c a
c d
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=ap.__version__)
    sequences_pathname = arguments["<sequences>"]  # type: ignore
    plots_prefix_pathname = arguments["<prefix>"]  # type: ignore
    output_format = arguments["--format"]  # type: ignore

    return plot_graphs(sequences_pathname, plots_prefix_pathname, output_format)
