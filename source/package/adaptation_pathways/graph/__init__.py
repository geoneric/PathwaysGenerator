import copy

from ..action_conversion import ActionConversion
from .io import read_sequences  # noqa: F401
from .layout import pathway_graph_layout, sequence_graph_layout  # noqa: F401
from .pathway_graph import PathwayGraph
from .pathway_map import PathwayMap
from .plot import (  # noqa: F401
    plot_and_save_pathway_graph,
    plot_and_save_pathway_map,
    plot_and_save_sequence_graph,
    plot_pathway_graph,
    plot_pathway_map,
    plot_sequence_graph,
)
from .sequence_graph import SequenceGraph


def sequence_graph_to_pathway_graph(sequence_graph: SequenceGraph) -> PathwayGraph:
    def visit_graph(
        sequence_graph: SequenceGraph,
        pathway_graph: PathwayGraph,
        from_action,
        to_action,
    ):
        conversion = ActionConversion(from_action, to_action)

        if sequence_graph.nr_from_actions(from_action) == 0:
            pathway_graph.start_pathway(from_action, conversion)

        if sequence_graph.nr_to_actions(to_action) == 0:
            pathway_graph.end_pathway(conversion, to_action)
        else:
            for to_action_new in sequence_graph.to_actions(to_action):
                to_tipping_point = visit_graph(
                    sequence_graph, pathway_graph, to_action, to_action_new
                )
                pathway_graph.add_period(conversion, to_tipping_point)

        return conversion

    # - The root node of the action graph must end up in the pathway graph as the root node
    # - Each leaf node of the actions graph (that is not also a root node) must end up as a
    #   leaf node in the pathway graph
    # - Each edge in the actions graph must end up as a node in the pathway graph

    pathway_graph = PathwayGraph()

    if sequence_graph.nr_actions() > 0:
        root_action = sequence_graph.root_node

        for to_action in sequence_graph.to_actions(root_action):
            visit_graph(sequence_graph, pathway_graph, root_action, to_action)

    return pathway_graph


def pathway_graph_to_pathway_map(pathway_graph: PathwayGraph) -> PathwayMap:
    def visit_graph(
        pathway_graph: PathwayGraph,
        pathway_map: PathwayMap,
        from_tipping_point,
    ):
        pathway_graph_nx = pathway_graph.graph

        # Collection of actions, defined by from/to tipping points
        actions = list(pathway_graph_nx.out_edges(from_tipping_point))

        if len(actions) == 1:
            pathway_map.add_action(from_tipping_point, actions[0][1])
            visit_graph(pathway_graph, pathway_map, actions[0][1])
        elif len(actions) > 1:
            # In case the action is followed by more than one pathway, we need to duplicate the
            # tipping point. This will end up as the forking point on the vertical line in the
            # pathways map.
            to_tipping_point = copy.deepcopy(from_tipping_point)
            pathway_map.add_action(from_tipping_point, to_tipping_point)

            for action in actions:
                pathway_map.add_action(to_tipping_point, action[1])
                visit_graph(pathway_graph, pathway_map, action[1])

    pathway_map = PathwayMap()

    if pathway_graph.nr_nodes() > 0:
        root_conversion = pathway_graph.root_node

        visit_graph(pathway_graph, pathway_map, root_conversion)

    return pathway_map
