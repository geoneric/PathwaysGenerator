import itertools

import numpy as np

from ..action import Action
from ..action_conversion import ActionConversion
from .layout import distribute, sort_horizontally
from .pathway_graph import PathwayGraph


# A pathway graph contains zero or more pathways: sequences of actions with conversions
# between each pair of actions. Each of those sequences starts with an action and ends with an
# action. All sequences start with the same action ("current"). Some of them may end with the
# same action.

# Think in terms of periods: sequences of action-conversion, action, action-conversion
# - In the end, the position of conversions depend on tipping points
# - Position actions just halfway between the conversions

# A pathway graph is layed out as follow:
#
# Horizontally:
# - The root action is located at 0
# - Its to-conversions are located at x = x + 1
# - Their actions are located at x = x + 1
# - Their to-conversions are located at x = x + 1
# - Recurse, similar to sequence graph. Push stuff to the right if necessary, depending on
#   the in-degree.
#
# Vertically
# - The root action is located at 0
# - Its to-actions are vertically sorted, around y==0
# - Their conversions are located halfway
# - Their to-conversions are vertically sorted, around their action's y-coordinate
# - Recurse, similar to sequence graph. Redistribute stuff vertically if necessary, depending
#   on the distance between the y-coordinates at the same x-coordinate.


def add_position(
    position_by_node: dict[Action | ActionConversion, np.ndarray],
    conversion: Action | ActionConversion,
    position: tuple[float, float],
) -> None:
    position_by_node[conversion] = np.array(position, np.float64)


def distribute_horizontally(
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
        distribute_horizontally(pathway_graph, to_conversion, position_by_node)


def distribute_vertically(
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


def pathway_graph_layout(
    pathway_graph: PathwayGraph,
) -> dict[Action | ActionConversion, np.ndarray]:
    position_by_node: dict[Action | ActionConversion, np.ndarray] = {}

    if pathway_graph.nr_conversions() > 0:
        from_conversion = pathway_graph.root_node
        add_position(position_by_node, from_conversion, (0, 0))
        distribute_horizontally(pathway_graph, from_conversion, position_by_node)
        distribute_vertically(pathway_graph, from_conversion, position_by_node)

    return position_by_node

    # def visit_graph(
    #     pathway_graph: PathwayGraph,
    #     from_conversion: Action | ActionConversion,
    #     to_conversion: ActionConversion | Action,
    #     coordinates: tuple[float, float],
    #     position_by_node: dict[Action, np.ndarray],
    # ):
    #     x, y = coordinates

    #     if from_conversion not in position_by_node:
    #         add_position(position_by_node, from_conversion, (x, y))

    #     x += 1

    #     if to_conversion not in position_by_node:
    #         add_position(position_by_node, to_conversion, (x, y))

    #     if pathway_graph.nr_to_conversions(to_conversion) > 0:
    #         # x += 1

    #         for to_tipping_point_new in pathway_graph.to_conversions(to_conversion):
    #             visit_graph(
    #                 pathway_graph,
    #                 to_conversion,
    #                 to_tipping_point_new,
    #                 (x, y),
    #                 position_by_node,
    #             )
    #             y -= 1

    # position_by_node: dict[Action, np.ndarray] = {}

    # if pathway_graph.nr_conversions() > 0:
    #     root_action = pathway_graph.root_node
    #     x, y = 0, 0

    #     for to_conversion in pathway_graph.to_conversions(root_action):
    #         visit_graph(pathway_graph, root_action, to_conversion, (x, y), position_by_node)
    #         y -= 1

    # return position_by_node
