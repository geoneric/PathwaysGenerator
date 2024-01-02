import itertools

import numpy as np

from ..node import Action, ActionConversion
from ..pathway_graph import PathwayGraph
from .util import add_position, distribute, sort_horizontally


def _distribute_horizontally(
    pathway_graph: PathwayGraph,
    from_conversion: Action | ActionConversion,
    position_by_node: dict[Action | ActionConversion, np.ndarray],
) -> None:
    min_distance = 1.0
    from_x = position_by_node[from_conversion][0]

    for to_conversion in pathway_graph.to_conversions(from_conversion):
        to_x = from_x + min_distance

        # Push conversion to the right if necessary
        if to_conversion in position_by_node:
            to_x = max(to_x, position_by_node[to_conversion][0])

        add_position(position_by_node, to_conversion, (to_x, np.nan))

    for to_conversion in pathway_graph.to_conversions(from_conversion):
        _distribute_horizontally(pathway_graph, to_conversion, position_by_node)


def _distribute_vertically(
    pathway_graph: PathwayGraph,
    from_action: Action,
    position_by_node: dict[Action | ActionConversion, np.ndarray],
) -> None:
    # Visit *all* actions and conversions in one go, in order of increasing x-coordinate
    # - Group actions and conversions by x-coordinate. Within each group:
    #     - For each action or conversion to position, take the mean y-coordinates of all
    #       from-actions and from_conversions into account
    #     - Take some minimum distance into account. Move nodes that are too close to each other.

    min_distance = 1.0
    nodes = pathway_graph.all_to_actions_and_conversions(from_action)
    sorted_nodes, _ = sort_horizontally(nodes, position_by_node)

    # Iterate over sorted_nodes, grouped by their x-coordinate
    for _, grouped_sorted_nodes in itertools.groupby(  # type: ignore
        sorted_nodes,
        lambda action_or_conversion: position_by_node[action_or_conversion][0],
    ):
        nodes = list(grouped_sorted_nodes)

        # Initialize the y-coordinate with the mean of the y-coordinates of the nodes
        # that end in each node
        for node in nodes:
            # Each node is only visited once
            assert np.isnan(position_by_node[node][1])

            # Calculate the mean y-coordinate of actions that end in the to_action
            from_nodes = pathway_graph.from_nodes(node)

            # Only the root node does not have from_nodes
            assert len(from_nodes) > 0

            y_coordinates = [position_by_node[node][1] for node in from_nodes]

            # All from_nodes must already be positioned
            assert all(not np.isnan(coordinate) for coordinate in y_coordinates)

            mean_y = sum(position_by_node[node][1] for node in from_nodes) / len(
                from_nodes
            )
            position_by_node[node][1] = mean_y

        # If the previous loop resulted in same / similar y-coordinates, we spread them
        # out some more
        y_coordinates = [position_by_node[node][1] for node in nodes]
        y_coordinates = distribute(list(y_coordinates), min_distance)

        for idx, node in enumerate(nodes):
            assert not np.isnan(position_by_node[node][1])
            position_by_node[node][1] = y_coordinates[idx]


def default_layout(
    pathway_graph: PathwayGraph,
) -> dict[Action | ActionConversion, np.ndarray]:
    """
    Layout for visualizing pathway graphs

    :param pathway_graph: Pathway graph
    :return: Node positions

    The goal of this layout is to be able to visualize the contents of the graph.
    """
    position_by_node: dict[Action | ActionConversion, np.ndarray] = {}

    if pathway_graph.nr_conversions() > 0:
        from_conversion = pathway_graph.root_node
        add_position(position_by_node, from_conversion, (0, 0))
        _distribute_horizontally(pathway_graph, from_conversion, position_by_node)
        _distribute_vertically(pathway_graph, from_conversion, position_by_node)

    return position_by_node
