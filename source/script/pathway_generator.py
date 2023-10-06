#!/usr/bin/env python3
import os.path
import sys

import docopt

from adaptation_pathways import __version__, view_in_browser, view_in_window


def main() -> int:
    usage = """\
TODO

Usage:
    {command} [--port=<port>] (browser | window)
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

    port_nr = int(arguments["--port"])  # type: ignore

    status = 1

    if arguments["browser"]:  # type: ignore
        status = view_in_browser(port_nr)
    # elif arguments["jupyter"]:
    #     print(arguments)
    #     url = arguments["--url"] if arguments["--url"] is not None else ""
    #     mode = arguments["--mode"] if arguments["--mode"] is not None else ""
    #     status = view_in_jupyter(mode=mode, url=url)
    elif arguments["window"]:  # type: ignore
        status = view_in_window(port_nr)

    return status

    # - open existing pathway file
    # - start with empty pathway (condition based)
    # - start with empty pathway (time based)

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


if __name__ == "__main__":
    sys.exit(main())
