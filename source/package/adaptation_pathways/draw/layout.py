import numpy as np

from ..action import Action
from ..actions_graph import ActionsGraph
from ..pathways_graph import PathwaysGraph
from ..pathways_map import PathwaysMap


def actions_graph_layout(actions_graph: ActionsGraph) -> dict[Action, np.ndarray]:
    def visit_graph(
        actions_graph: ActionsGraph,
        from_action: Action,
        to_action: Action,
        coordinates: tuple[float, float],
        nodes: dict[Action, np.ndarray],
    ):
        x, y = coordinates

        if from_action not in nodes:
            nodes[from_action] = np.array([x, y], dtype=np.float64)

        x += 1

        if to_action not in nodes:
            nodes[to_action] = np.array([x, y], dtype=np.float64)

        if actions_graph.nr_to_actions(to_action) > 0:
            x += 1

            for to_action_new in actions_graph.to_actions(to_action):
                visit_graph(actions_graph, to_action, to_action_new, (x, y), nodes)
                y += 1

    nodes: dict[Action, np.ndarray] = {}

    if not actions_graph.is_empty:
        root_action = actions_graph.root_node
        x, y = 0, 0

        for to_action in actions_graph.to_actions(root_action):
            visit_graph(actions_graph, root_action, to_action, (x, y), nodes)
            y += 1

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

    if not pathways_graph.is_empty:
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

    if not pathways_map.is_empty:
        root_tipping_point = pathways_map.root_node
        x, y = 0, 0

        visit_graph(pathways_map, root_tipping_point, (x, y), nodes)

    return nodes
