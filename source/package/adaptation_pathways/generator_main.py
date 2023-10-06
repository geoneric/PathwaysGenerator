import os.path
import sys

import docopt
import pandas as pd

from .browser import view_in_browser  # noqa: F401

# from .jupyter import view_in_jupyter  # noqa: F401
from .networkx import plot_pathways as plot_pathways_nx
from .version import __version__
from .window import view_in_window  # noqa: F401


def plot_pathways(
    interventions_table_pathname,
    pathways_table_pathname,
    scenarios_table_pathname,
    pathways_plot_pathname,
) -> int:
    try:
        interventions_table = pd.read_csv(interventions_table_pathname)
        pathways_table = pd.read_csv(pathways_table_pathname)
        scenarios_table = pd.read_csv(scenarios_table_pathname)
        plot_pathways_nx(
            interventions_table, pathways_table, scenarios_table, pathways_plot_pathname
        )
        status = 0
    except Exception as error:  # pylint: disable=broad-exception-caught
        sys.stderr.write(f"Error occurred while plotting pathways:\n{str(error)}\n")
        status = 1

    return status


def generator_main() -> int:
    usage = """\
TODO

Usage:
    {command} [--port=<port>] (browser | window)
    {command} <interventions> <pathways> <scenarios> <plot>
    {command} -h | --help
    {command} --version

Options:
    -h --help      Show this screen
    --version      Show version
    --port=<port>  Port number [default: 8050]
""".format(
        command=os.path.basename(sys.argv[0])
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
