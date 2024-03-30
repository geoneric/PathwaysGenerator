#!/usr/bin/env python3
import os.path
import sys

import docopt

import adaptation_pathways as ap
import adaptation_pathways.plot.colour as ap_colour


def print_nord_theme_colours() -> None:
    print("rgba - argb as hex")

    print("nominal")
    for colour in ap_colour.nord_palette_nominal:
        print(f"{colour}\t{ap_colour.rgba_to_hex(colour)}")

    print("dark")
    for colour in ap_colour.nord_palette_dark:
        print(f"{colour}\t{ap_colour.rgba_to_hex(colour)}")

    print("light")
    for colour in ap_colour.nord_palette_light:
        print(f"{colour}\t{ap_colour.rgba_to_hex(colour)}")

    print("blue")
    for colour in ap_colour.nord_palette_blue:
        print(f"{colour}\t{ap_colour.rgba_to_hex(colour)}")


def main() -> None:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Print colours from the nord theme in different formats

Usage:
    {command}

Options:
    -h --help        Show this screen and exit
    --version        Show version and exit
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=ap.__version__)

    print_nord_theme_colours()


if __name__ == "__main__":
    main()
