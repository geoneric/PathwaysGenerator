import os.path
import sys
from pathlib import Path

import docopt

from ..io import sqlite, text
from ..version import __version__ as version
from .main import main_function


# Current issue:
# TODO Merge tipping points (optional) with sequences. Get rid of tipping points table.
# TODO Support writing tipping points to database
# TODO Support writing action combinations to database
# TODO Update all cli to use text.read_dataset and sqlite.read_dataset
# TODO Use argb everywhere?
# TODO Get rid of Action's edition


# New issue:
# TODO Update sequence graph to show connections between actions,
#      whatever the timing. Uniqueness doesn't matter at all, only the name.
#      Goal is to show dependencies between actions. Graph statistics.


@main_function
def import_(basename_pathname: str, dataset_pathname: str) -> int:

    actions, sequences, tipping_point_by_action, colour_by_action = text.read_dataset(
        basename_pathname
    )

    sqlite.write_dataset(
        actions,
        sequences,
        tipping_point_by_action,
        colour_by_action,
        Path(dataset_pathname),
    )

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Import text files to dataset

Usage:
    {command} <basename> <dataset>

Arguments:
    basename           Name, without postfix and extension of group of files
                       to import from
    dataset            Pathname of dataset to import to. If the dataset
                       already exists, it will be overwritten.

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit

Example:
    {command} serial serial.apw

This example imports information from the following files:
- serial-action.txt → Contains information about each action (required)
- serial-sequence.txt → Contains the sequences that make up pathways
  (required)
- serial-tipping_point.txt → Contains tipping points for each action edition
  (optional)

Information about how information in these file should be formatted can be
found in the documentation.
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=version)
    basename_pathname = arguments["<basename>"]  # type: ignore
    dataset_pathname = arguments["<dataset>"]  # type: ignore

    return import_(basename_pathname, dataset_pathname)
