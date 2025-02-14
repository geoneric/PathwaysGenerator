import enum
import typing

import matplotlib as mpl

from ...graph import PathwayMap
from .classic import plot as plot_classic
from .default import plot as plot_default


PathwayMapLayout = enum.Enum("PathwayMapLayout", ["DEFAULT", "CLASSIC"])
"""
When plotting pathway maps, these constants can be used to select the correct layout
"""


def plot_pathway_map(
    axes: mpl.axes.Axes,
    pathway_map: PathwayMap,
    *,
    arguments: dict[str, typing.Any] | None = None,
    # plot_colours: PlotColours | None = None,
) -> None:
    """
    Plot a pathway map

    Based on the layout passed in, the pathway map is plotted using the default or "classic"
    layout.

    See also:
        :func:`default.plot <adaptation_pathways.plot.pathway_map.default.plot>`
        :func:`classic.plot <adaptation_pathways.plot.pathway_map.classic.plot>`
    """
    if arguments is None:
        arguments = {}

    arguments.setdefault("layout", PathwayMapLayout.DEFAULT)

    layout = arguments["layout"]

    if layout == PathwayMapLayout.CLASSIC:
        plot_classic(axes, pathway_map, arguments=arguments)
    else:
        plot_default(axes, pathway_map, arguments=arguments)
