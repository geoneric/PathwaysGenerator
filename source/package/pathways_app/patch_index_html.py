import sys
from pathlib import Path

import docopt


def main() -> int:
    command = Path(sys.argv[0]).name
    usage = f"""\
Patch web app's index.html

Usage:
    {command} <pathname>

Arguments:
    pathname        Pathname of index.html file to patch

Options:
    -h --help       Show this screen and exit
"""
    status = 1

    try:
        arguments = sys.argv[1:]
        arguments = docopt.docopt(usage, arguments)
        html_pathname = arguments["<pathname>"]  # type: ignore

        search_for = '<script src="python.js"></script>'
        replace_with = f'{search_for}\n  <script src="js/pathways.js"></script>'

        path = Path(html_pathname)
        content = path.read_text(encoding="utf-8")
        content = content.replace(search_for, replace_with)
        path.write_text(content, encoding="utf-8")

        status = 0
    except Exception as exception:
        sys.stderr.write(f"{exception}\n")

    return status


if __name__ == "__main__":
    sys.exit(main())
