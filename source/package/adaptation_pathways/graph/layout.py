import itertools

import numpy as np

from ..action import Action
from .coordinate import distribute
from .pathways_graph import PathwaysGraph
from .pathways_map import PathwaysMap
from .sequence_graph import SequenceGraph


def add_position(nodes, action, position):
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


def sort_horizontally(
    actions: list[Action], nodes: dict[Action, np.ndarray]
) -> tuple[list[Action], list[float]]:
    sorted_actions = []
    x_coordinates = []

    if len(actions) > 0:
        x_coordinates = [nodes[action][0] for action in actions]
        action_coordinate_pairs = sorted(
            zip(actions, x_coordinates), key=lambda pair: pair[1]
        )
        sorted_actions, x_coordinates = zip(*action_coordinate_pairs)

    return sorted_actions, x_coordinates


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

        # First (lowest) y_coordinate corresponds with the last to_action. Therefore,
        # reverse 'm.
        y_coordinates = list(reversed(y_coordinates))

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


def pathways_graph_layout(pathways_graph: PathwaysGraph) -> dict[Action, np.ndarray]:
    def visit_graph(
        pathways_graph: PathwaysGraph,
        from_tipping_point: Action,
        to_tipping_point: Action,
        coordinates: tuple[float, float],
        nodes: dict[Action, np.ndarray],
    ):
        x, y = coordinates

        if from_tipping_point not in nodes:
            nodes[from_tipping_point] = np.array([x, y], dtype=np.float64)

        x += 1

        if to_tipping_point not in nodes:
            nodes[to_tipping_point] = np.array([x, y], dtype=np.float64)

        if pathways_graph.nr_to_tipping_points(to_tipping_point) > 0:
            x += 1

            for to_tipping_point_new in pathways_graph.to_tipping_points(
                to_tipping_point
            ):
                visit_graph(
                    pathways_graph,
                    to_tipping_point,
                    to_tipping_point_new,
                    (x, y),
                    nodes,
                )
                y += 1

    nodes: dict[Action, np.ndarray] = {}

    if pathways_graph.nr_nodes() > 0:
        root_tipping_point = pathways_graph.root_node
        x, y = 0, 0

        for to_tipping_point in pathways_graph.to_tipping_points(root_tipping_point):
            visit_graph(
                pathways_graph, root_tipping_point, to_tipping_point, (x, y), nodes
            )
            y += 1

    return nodes


def pathways_map_layout(pathways_map: PathwaysMap) -> dict[Action, np.ndarray]:
    def visit_graph(
        pathways_map: PathwaysMap,
        from_tipping_point: Action,
        coordinates: tuple[float, float],
        nodes: dict[Action, np.ndarray],
    ):
        x, y = coordinates

        if from_tipping_point not in nodes:
            nodes[from_tipping_point] = np.array([x, y], dtype=np.float64)

        x += 1

        to_tipping_point = pathways_map.to_tipping_point(from_tipping_point)

        if to_tipping_point not in nodes:
            nodes[to_tipping_point] = np.array([x, y], dtype=np.float64)

        for from_tipping_point_new in pathways_map.from_tipping_points(
            to_tipping_point
        ):
            if pathways_map.nr_downstream_actions(from_tipping_point_new) == 0:
                if from_tipping_point_new not in nodes:
                    nodes[from_tipping_point_new] = np.array(
                        [x + 1, y], dtype=np.float64
                    )
            else:
                y += 1
                visit_graph(pathways_map, from_tipping_point_new, (x, y), nodes)

    nodes: dict[Action, np.ndarray] = {}

    if pathways_map.nr_nodes() > 0:
        root_tipping_point = pathways_map.root_node
        x, y = 0, 0

        visit_graph(pathways_map, root_tipping_point, (x, y), nodes)

    return nodes
