import os.path
import sys
import typing

import docopt
import matplotlib.pyplot as plt

from ..graph import SequenceGraph, sequence_graph_to_pathway_map, verify_tipping_points
from ..io import read_dataset
from ..plot import init_axes, plot_bars, save_plot
from ..plot.util import action_level_by_first_occurrence
from ..version import __version__ as version
from .main import main_function


@main_function
def plot_bars_(
    basename_pathname: str,
    plot_pathname: str,
    *,
    arguments,
    legend_arguments,
) -> int:

    # pylint: disable-next=unused-variable
    _, sequences, tipping_point_by_action, colour_by_action = read_dataset(
        basename_pathname
    )

    colour_by_action_name = {
        action.name: colour for action, colour in colour_by_action.items()
    }

    level_by_action = action_level_by_first_occurrence(sequences)
    sequence_graph = SequenceGraph(sequences)
    pathway_map = sequence_graph_to_pathway_map(sequence_graph)

    verify_tipping_points(pathway_map, tipping_point_by_action)

    _, axes = plt.subplots(layout="constrained")
    init_axes(axes)

    arguments["colour_by_action_name"] = colour_by_action_name
    arguments["level_by_action"] = level_by_action
    arguments["tipping_point_by_action"] = tipping_point_by_action

    plot_bars(axes, pathway_map, arguments=arguments, legend_arguments=legend_arguments)
    save_plot(plot_pathname)

    return 0


def parse_spread(spread: str) -> tuple[float, float]:
    spreads = spread.split(",")

    if len(spreads) == 1:
        result = float(spreads[0]), float(spreads[0])
    else:
        assert (
            len(spreads) == 2
        ), "Pass in a single floating point value, or two separated by a comma"
        result = float(spreads[0]), float(spreads[1])

    return result


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Plot bars

Usage:
    {command} [--title=<title>] [--x_label=<label>] [--show_legend]
        [--stack_bars] <basename> <plot>

Arguments:
    basename           Either, the name without postfix and extension of text
                       file(s) to read information from, or the name of a
                       binary file to read information from.
    plot               Name of file to store plot in. The format will be
                       based on the extension of the name passed in. The
                       default, when no extension is present, is pdf.

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit
    --show_legend      Show legend
    --stack_bars       Stack bars
    --title=<title>    Title
    --x_label=<label>  Label of x-axis

The format for storing sequences is simple: per line mention the names of
two actions that form a sequence. Information from multiple lines can result
in longer sequences. To allow for the same action to occur in different
sequences, a number can be added to the name.

Examples:
    {command} serial serial.pdf
    {command} serial.apw serial.pdf
"""
    arguments = docopt.docopt(usage, sys.argv[1:], version=version)
    basename_pathname = arguments["<basename>"]
    plot_pathname = arguments["<plot>"]
    title = arguments["--title"] if arguments["--title"] is not None else ""
    x_label = arguments["--x_label"] if arguments["--x_label"] is not None else ""
    show_legend = arguments["--show_legend"]
    stack_bars = arguments["--stack_bars"]

    plot_arguments: dict[str, typing.Any] = {
        "title": title,
        "x_label": x_label,
        "show_legend": show_legend,
        "stack_bars": stack_bars,
    }

    if len(os.path.splitext(plot_pathname)[1]) == 0:
        plot_pathname += ".pdf"

    # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html#matplotlib.axes.Axes.legend
    legend_arguments = {
        "framealpha": 0.5,
        "fancybox": False,
    }

    return plot_bars_(
        basename_pathname,
        plot_pathname,
        arguments=plot_arguments,
        legend_arguments=legend_arguments,
    )
