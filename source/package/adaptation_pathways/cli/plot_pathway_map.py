import os.path
import sys

import docopt

from ..graph.conversion import sequence_graph_to_pathway_map
from ..graph.io import read_sequences, read_tipping_points
from ..graph.plot import PathwayMapLayout, plot_and_save_pathway_map
from ..version import __version__ as version
from .main import main_function


@main_function
def plot_map(
    sequences_pathname: str, tipping_points_pathname: str, plot_pathname: str
) -> int:
    sequence_graph, level_by_action = read_sequences(sequences_pathname)
    pathway_map = sequence_graph_to_pathway_map(sequence_graph)
    tipping_points = read_tipping_points(tipping_points_pathname, pathway_map.actions())

    pathway_map.assign_tipping_points(tipping_points, verify=True)
    pathway_map.set_attribute("level", level_by_action)

    plot_and_save_pathway_map(
        pathway_map, plot_pathname, layout=PathwayMapLayout.CLASSIC
    )

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Plot pathway map

Usage:
    {command} <sequences> <tipping_points> <plot>

Arguments:
    sequences          Name of file containing sequences of actions
    tipping_points     Name of file containing tipping points
    plot               Name of file to store plot. The format will be
                       based on the extension of the name passed in. The
                       default, when no extension is present, is pdf.

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit

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

The format for storing tipping points is also very simple: per line mention
the name of an action and a tipping point. Tipping points are whole numbers.
All actions mentioned in the sequences file must be present in the tipping
point file.

Example:

current 2020
a 2060
b1 2040
c 2050
d 2060
b2 2060
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=version)
    sequences_pathname = arguments["<sequences>"]  # type: ignore
    tipping_points_pathname = arguments["<tipping_points>"]  # type: ignore
    plot_pathname = arguments["<plot>"]  # type: ignore

    if len(os.path.splitext(plot_pathname)[1]) == 0:
        plot_pathname += ".pdf"

    return plot_map(sequences_pathname, tipping_points_pathname, plot_pathname)
