import matplotlib as mpl
import numpy as np

from ...graph import PathwayMap
from ...graph.node import Node
from ..colour import PlotColours
from ..util import add_position, distribute, plot_graph
from .colour import default_colours


def _distribute_horizontally(
    pathway_map: PathwayMap,
    position_by_node: dict[Node, np.ndarray],
) -> None:
    """
    Assign x-coordinates to all action_{begin,end} nodes in the pathway map
    """

    paths = pathway_map.all_paths()

    if len(paths) > 0:
        min_distance = 1.0

        for path in paths:
            begin_x = 0.0
            end_x = begin_x + min_distance

            for action_begin_idx in range(0, len(path), 2):
                action_begin, action_end = (
                    path[action_begin_idx],
                    path[action_begin_idx + 1],
                )
                add_position(position_by_node, action_begin, (begin_x, np.nan))
                add_position(position_by_node, action_end, (end_x, np.nan))
                begin_x = end_x + min_distance
                end_x = begin_x + min_distance


def _distribute_vertically(
    pathway_map: PathwayMap,
    position_by_node: dict[Node, np.ndarray],
) -> None:
    paths = pathway_map.all_paths()
    min_distance = 1.0
    y_coordinates = distribute([0.0] * len(paths), min_distance)

    for path_idx, path in enumerate(paths):
        y_coordinate = y_coordinates[path_idx]

        for node in path:
            position_by_node[node][1] = y_coordinate


def _layout(
    pathway_map: PathwayMap,
) -> dict[Node, np.ndarray]:
    """
    Layout for visualizing pathway maps

    :param pathway_map: Pathway map
    :return: Node positions

    The goal of this layout is to be able to visualize the contents of the graph.
    """
    position_by_node: dict[Node, np.ndarray] = {}

    if pathway_map.nr_edges() > 0:
        _distribute_horizontally(pathway_map, position_by_node)
        _distribute_vertically(pathway_map, position_by_node)

    return position_by_node


def plot(
    axes: mpl.axes.Axes,
    pathway_map: PathwayMap,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    if plot_colours is None:
        plot_colours = default_colours(pathway_map)

    plot_graph(
        axes,
        pathway_map.graph,
        title,
        _layout(pathway_map),
        plot_colours,
    )
