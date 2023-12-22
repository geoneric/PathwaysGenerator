import itertools

import numpy as np

from ..node import Action
from ..sequence_graph import SequenceGraph
from .util import distribute, sort_horizontally


def add_position(
    nodes: dict[Action, np.ndarray], action: Action, position: tuple[float, float]
) -> None:
    nodes[action] = np.array(position, np.float64)


def distribute_horizontally(
    sequence_graph: SequenceGraph,
    from_action: Action,
    nodes: dict[Action, np.ndarray],
) -> None:
    min_distance = 1.0
    from_x = nodes[from_action][0]

    for to_action in sequence_graph.to_actions(from_action):
        to_x = from_x + min_distance

        # Push action to the right if necessary
        if to_action in nodes:
            to_x = max(to_x, nodes[to_action][0])

        add_position(nodes, to_action, (to_x, np.nan))

    for to_action in sequence_graph.to_actions(from_action):
        distribute_horizontally(sequence_graph, to_action, nodes)


def distribute_vertically(
    sequence_graph: SequenceGraph,
    from_action: Action,
    nodes: dict[Action, np.ndarray],
) -> None:
    # Visit *all* actions in one go, in order of increasing x-coordinate
    # - Group actions by x-coordinate. Within each group:
    #     - For each action to position, take the mean y-coordinates of all from-actions
    #       into account
    #     - Take some minimum distance into account. Move nodes that are too close to each other.

    min_distance = 1.0
    actions = sequence_graph.all_to_actions(from_action)
    sorted_actions, _ = sort_horizontally(actions, nodes)

    # Iterate over to_action_coordinate_pairs, grouped by their x-coordinate
    for _, grouped_sorted_actions in itertools.groupby(  # type: ignore
        sorted_actions, lambda action: nodes[action][0]
    ):
        actions = list(grouped_sorted_actions)

        # Initialize the y-coordinate with the mean of the y-coordinates of the from_actions
        # that end in each action
        for action in actions:
            # Each action is only visited once
            assert np.isnan(nodes[action][1])

            # Calculate the mean y-coordinate of actions that end in the to_action
            from_actions = sequence_graph.from_actions(action)

            # Only the root action does not have from_actions
            assert len(from_actions) > 0

            y_coordinates = [nodes[action][1] for action in from_actions]

            # All from_actions must already be positioned
            assert all(not np.isnan(coordinate) for coordinate in y_coordinates)

            mean_y = sum(nodes[action][1] for action in from_actions) / len(
                from_actions
            )
            nodes[action][1] = mean_y

        # If the previous loop resulted in same / similar y-coordinates, we spread them
        # out some more
        y_coordinates = [nodes[action][1] for action in actions]
        y_coordinates = distribute(list(y_coordinates), min_distance)

        for idx, action in enumerate(actions):
            assert not np.isnan(nodes[action][1])
            nodes[action][1] = y_coordinates[idx]


def sequence_graph_layout(sequence_graph: SequenceGraph) -> dict[Action, np.ndarray]:
    nodes: dict[Action, np.ndarray] = {}

    if sequence_graph.nr_actions() > 0:
        from_action = sequence_graph.root_node
        add_position(nodes, from_action, (0, 0))
        distribute_horizontally(sequence_graph, from_action, nodes)
        distribute_vertically(sequence_graph, from_action, nodes)

    return nodes
