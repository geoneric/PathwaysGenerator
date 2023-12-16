import copy

from ..sequenced_action import SequencedAction
from .io import read_sequences  # noqa: F401
from .layout import sequence_graph_layout  # noqa: F401
from .pathways_graph import PathwaysGraph
from .pathways_map import PathwaysMap
from .plot import (  # noqa: F401
    plot_and_save_sequence_graph,
    plot_pathways_graph,
    plot_pathways_map,
    plot_sequence_graph,
)
from .sequence_graph import SequenceGraph


def sequence_graph_to_pathways_graph(sequence_graph: SequenceGraph) -> PathwaysGraph:
    def visit_graph(
        sequence_graph: SequenceGraph,
        pathways_graph: PathwaysGraph,
        from_action,
        to_action,
    ):
        sequence_graph_nx = sequence_graph.graph
        tipping_point = SequencedAction(from_action, to_action)

        if sequence_graph_nx.in_degree(from_action) == 0:
            pathways_graph.add_action(from_action, tipping_point)

        if sequence_graph_nx.out_degree(to_action) == 0:
            pathways_graph.add_action(tipping_point, to_action)
        else:
            for to_action_new in sequence_graph_nx.adj[to_action]:
                to_tipping_point = visit_graph(
                    sequence_graph, pathways_graph, to_action, to_action_new
                )
                pathways_graph.add_action(tipping_point, to_tipping_point)

        return tipping_point

    # - The root node of the action graph must end up in the pathways graph as the root node
    # - Each leaf node of the actions graph (that is not also a root node) must end up as a
    #   leaf node in the pathways graph
    # - Each edge in the actions graph must end up as a node in the pathways graph

    pathways_graph = PathwaysGraph()

    if sequence_graph.nr_actions() > 0:
        sequence_graph_nx = sequence_graph.graph
        root_action = sequence_graph.root_node

        for to_action in sequence_graph_nx.adj[root_action]:
            visit_graph(sequence_graph, pathways_graph, root_action, to_action)

    return pathways_graph


def pathways_graph_to_pathways_map(pathways_graph: PathwaysGraph) -> PathwaysMap:
    def visit_graph(
        pathways_graph: PathwaysGraph,
        pathways_map: PathwaysMap,
        from_tipping_point,
    ):
        pathways_graph_nx = pathways_graph.graph

        # Collection of actions, defined by from/to tipping points
        actions = list(pathways_graph_nx.out_edges(from_tipping_point))

        if len(actions) == 1:
            pathways_map.add_action(from_tipping_point, actions[0][1])
            visit_graph(pathways_graph, pathways_map, actions[0][1])
        elif len(actions) > 1:
            # In case the action is followed by more than one pathway, we need to duplicate the
            # tipping point. This will end up as the forking point on the vertical line in the
            # pathways map.
            to_tipping_point = copy.deepcopy(from_tipping_point)
            pathways_map.add_action(from_tipping_point, to_tipping_point)

            for action in actions:
                pathways_map.add_action(to_tipping_point, action[1])
                visit_graph(pathways_graph, pathways_map, action[1])

    pathways_map = PathwaysMap()

    if pathways_graph.nr_nodes() > 0:
        root_conversion = pathways_graph.root_node

        visit_graph(pathways_graph, pathways_map, root_conversion)

    return pathways_map
