import numpy as np

from ..action import Action
from ..pathways_graph import PathwaysGraph


def visit_pathways_graph_edge(
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
            visit_pathways_graph_edge(
                pathways_graph, to_tipping_point, to_tipping_point_new, (x, y), nodes
            )


def pathways_graph_layout(pathways_graph: PathwaysGraph) -> dict[Action, np.ndarray]:
    pathways_graph_nx = pathways_graph.graph
    nodes: dict[Action, np.ndarray] = {}

    if not pathways_graph.is_empty:
        x = 0.0
        y = 0.0
        root_tipping_point = pathways_graph.root_node

        for to_tipping_point in pathways_graph_nx.adj[root_tipping_point]:
            visit_pathways_graph_edge(
                pathways_graph, root_tipping_point, to_tipping_point, (x, y), nodes
            )
            y += 1

    # nodes must be layed out in vertically, depending on
    # - The tipping points
    # - From action in the sequenced action

    # Don't just grab all nodes, but walk along the pathways and layout the nodes one after
    # the other. Calculate the tipping points for now.

    # for node in pathways_graph_nx.nodes:
    #     nodes[node] = np.array([x, y], dtype=np.float64)
    #     y += 1

    return nodes
