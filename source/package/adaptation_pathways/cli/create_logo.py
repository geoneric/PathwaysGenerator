import os.path
import sys
from io import StringIO

import docopt
import matplotlib.pyplot as plt

from ..graph.conversion import (
    sequence_graph_to_pathway_map,
    sequences_to_sequence_graph,
)
from ..graph.io import (
    action_level_by_first_occurrence,
    read_sequences,
    read_tipping_points,
)
from ..plot import init_axes, plot_classic_pathway_map, save_plot
from ..version import __version__ as version
from .main import main_function


@main_function
def create_logo(plot_pathname: str) -> int:
    sequences = read_sequences(
        StringIO(
            """
a b
a c
a d
c d
"""
        )
    )
    sequence_graph = sequences_to_sequence_graph(sequences)
    level_by_action = action_level_by_first_occurrence(sequences)
    pathway_map = sequence_graph_to_pathway_map(sequence_graph)
    tipping_points = read_tipping_points(
        StringIO(
            """
a 2040
b 2050
c 2060
d 2070
"""
        ),
        pathway_map.actions(),
    )

    pathway_map.assign_tipping_points(tipping_points)
    pathway_map.set_attribute("level", level_by_action)

    _, axes = plt.subplots(layout="constrained")
    init_axes(axes)
    plot_classic_pathway_map(axes, pathway_map)

    save_plot(plot_pathname + ".pdf")
    save_plot(plot_pathname + ".svg")

    # TODO Create raster images in various resolutions.

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Create logo

Usage:
    {command} <logo>

Arguments:
    logo            Basename of file to store the logo in. Files with
                    different formats and resolutions will be created.

Options:
    -h --help       Show this screen and exit
    --version       Show version and exit
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=version)
    logo_pathname = arguments["<logo>"]  # type: ignore

    assert len(os.path.splitext(logo_pathname)[1]) == 0, "Please remove the extension"

    return create_logo(logo_pathname)
