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
        pathways_graph_nx = actions_graph.graph
        x, y = coordinates

        nodes[from_action] = np.array([x, y], dtype=np.float64)
        nodes[to_action] = np.array([x + 1, y], dtype=np.float64)

        if pathways_graph_nx.out_degree(to_action) == 0:
            pass
        else:
            x += 1
            for to_action_new in pathways_graph_nx.adj[to_action]:
                visit_graph(actions_graph, to_action, to_action_new, (x, y), nodes)

    nodes: dict[Action, np.ndarray] = {}

    if not actions_graph.is_empty:
        actions_graph_nx = actions_graph.graph
        x = 0.0
        y = 0.0
        root_action = actions_graph.root_node

        for to_action in actions_graph_nx.adj[root_action]:
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
        pathways_graph_nx = pathways_graph.graph
        x, y = coordinates

        nodes[from_tipping_point] = np.array([x, y], dtype=np.float64)
        nodes[to_tipping_point] = np.array([x + 1, y], dtype=np.float64)

        if pathways_graph_nx.out_degree(to_tipping_point) == 0:
            pass
        else:
            x += 1
            for to_tipping_point_new in pathways_graph_nx.adj[to_tipping_point]:
                visit_graph(
                    pathways_graph,
                    to_tipping_point,
                    to_tipping_point_new,
                    (x, y),
                    nodes,
                )

    nodes: dict[Action, np.ndarray] = {}

    if not pathways_graph.is_empty:
        pathways_graph_nx = pathways_graph.graph
        x = 0.0
        y = 0.0
        root_tipping_point = pathways_graph.root_node

        for to_tipping_point in pathways_graph_nx.adj[root_tipping_point]:
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
        pathways_map_nx = pathways_map.graph
        x, y = coordinates

        out_edges = list(pathways_map_nx.out_edges(from_tipping_point))

        assert len(out_edges) == 1, out_edges

        to_tipping_point: Action = out_edges[0][1]

        nodes[from_tipping_point] = np.array([x, y], dtype=np.float64)
        x += 1
        nodes[to_tipping_point] = np.array([x, y], dtype=np.float64)

        from_tipping_point = to_tipping_point

        for from_tipping_point_new in pathways_map_nx.out_edges(to_tipping_point):
            if len(pathways_map_nx.out_edges(from_tipping_point_new[1])) == 0:
                nodes[from_tipping_point_new[1]] = np.array(
                    [x + 1, y], dtype=np.float64
                )
            else:
                y += 1
                visit_graph(pathways_map, from_tipping_point_new[1], (x, y), nodes)

    nodes: dict[Action, np.ndarray] = {}

    if not pathways_map.is_empty:
        x = 0.0
        y = 0.0
        root_tipping_point = pathways_map.root_node

        visit_graph(pathways_map, root_tipping_point, (x, y), nodes)

    return nodes
