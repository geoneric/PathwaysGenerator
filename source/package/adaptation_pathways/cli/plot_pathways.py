import os.path
import sys

import docopt
import pandas as pd

from ..browser import view_in_browser  # noqa: F401

# from ..jupyter import view_in_jupyter  # noqa: F401
from ..networkx import plot_pathways as plot_pathways_nx
from ..version import __version__
from ..window import view_in_window  # noqa: F401
from .main import common_arguments, main_function


@main_function
def plot_pathways(
    interventions_table_pathname: str,
    pathways_table_pathname: str,
    scenarios_table_pathname: str,
    pathways_plot_pathname: str,
) -> int:
    """
    Plot pathways

    :param str interventions_table_pathname: Pathname of CSV file containing information about
        the interventions
    :param str pathways_table_pathname: Pathname of CSV file containing information about
        the pathways
    :param str scenarios_table_pathname: Pathname of CSV file containing information about
        the scenarios
    :param str pathways_plot_pathname: Pathname of output graphics file
    """
    interventions_table = pd.read_csv(interventions_table_pathname)
    pathways_table = pd.read_csv(pathways_table_pathname)
    scenarios_table = pd.read_csv(scenarios_table_pathname)
    plot_pathways_nx(
        interventions_table, pathways_table, scenarios_table, pathways_plot_pathname
    )
    return 0


def main() -> int:
    usage = """\
Generate adaptation pathways

Usage:
    {command} [--port=<port>] (browser | window)
    {command} <interventions> <pathways> <scenarios> <plot>
    {command} -h | --help
    {command} --version

Options:
{common_arguments}
    --port=<port>  Port number [default: 8050]
""".format(
        command=os.path.basename(sys.argv[0]),
        common_arguments=common_arguments,
    )
    # {command} [--url=<url>] [--mode=<mode>] jupyter

    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=__version__)

    status = 1

    if arguments["browser"] or arguments["window"]:  # type: ignore
        port_nr = int(arguments["--port"])  # type: ignore

        if arguments["browser"]:  # type: ignore
            status = view_in_browser(port_nr)
        # elif arguments["jupyter"]:
        #     print(arguments)
        #     url = arguments["--url"] if arguments["--url"] is not None else ""
        #     mode = arguments["--mode"] if arguments["--mode"] is not None else ""
        #     status = view_in_jupyter(mode=mode, url=url)
        elif arguments["window"]:  # type: ignore
            status = view_in_window(port_nr)
    else:
        interventions_table_pathname = arguments["<interventions>"]  # type: ignore
        pathways_table_pathname = arguments["<pathways>"]  # type: ignore
        scenarios_table_pathname = arguments["<scenarios>"]  # type: ignore
        pathways_plot_pathname = arguments["<plot>"]  # type: ignore

        status = plot_pathways(
            interventions_table_pathname,
            pathways_table_pathname,
            scenarios_table_pathname,
            pathways_plot_pathname,
        )

    return status

    # x-axis settings
    # - min value
    # - max value
    # - show tipping conditions axis (bool)
    # - x-axis caption
    # - ticks x-axis

    # Interface:
    # - action or pathway table
    # - pathway map
    # → Policy actions
    # - Tipping point
    # Add actions with their respective tipping points

    # Sequence stuff → pathways

    # Actions:
    # - Robust:
    #     - Insensitive to changing conditions
    # - Flexible:
    #     - Easily adaptable
    #     - Low associated costs
    #     - No major consequences for society

    # A pathway is a route into the future, taking into account each routes costs and consequences

    # 1. Choose approach (condition-based / time-based)
    # 2. Add actions
    # 3. Generate pathways
    # 4. Add scenarios
    # 5. Modify pathways
    # 6. Evaluate pathways
