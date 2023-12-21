import numpy as np

from ..action import Action
from .pathway_map import PathwayMap


def pathway_map_layout(pathway_map: PathwayMap) -> dict[Action, np.ndarray]:
    def visit_graph(
        pathway_map: PathwayMap,
        from_tipping_point: Action,
        coordinates: tuple[float, float],
        nodes: dict[Action, np.ndarray],
    ):
        x, y = coordinates

        if from_tipping_point not in nodes:
            nodes[from_tipping_point] = np.array([x, y], dtype=np.float64)

        x += 1

        to_tipping_point = pathway_map.to_tipping_point(from_tipping_point)

        if to_tipping_point not in nodes:
            nodes[to_tipping_point] = np.array([x, y], dtype=np.float64)

        for from_tipping_point_new in pathway_map.from_tipping_points(to_tipping_point):
            if pathway_map.nr_downstream_actions(from_tipping_point_new) == 0:
                if from_tipping_point_new not in nodes:
                    nodes[from_tipping_point_new] = np.array(
                        [x + 1, y], dtype=np.float64
                    )
            else:
                y += 1
                visit_graph(pathway_map, from_tipping_point_new, (x, y), nodes)

    nodes: dict[Action, np.ndarray] = {}

    if pathway_map.nr_nodes() > 0:
        root_tipping_point = pathway_map.root_node
        x, y = 0, 0

        visit_graph(pathway_map, root_tipping_point, (x, y), nodes)

    return nodes
