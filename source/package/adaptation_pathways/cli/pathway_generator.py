import os.path
import sys

import docopt

from ..desktop.application import application
from ..version import __version__


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Generate adaptation pathways

Usage:
    {command}
    {command} -h | --help
    {command} --version

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=__version__)
    status = application()

    return status
