import copy

from ..action import Action
from .colour import default_edge_colours, default_node_colours  # noqa: F401
from .io import read_sequences  # noqa: F401
from .pathway_graph import PathwayGraph
from .pathway_graph_layout import pathway_graph_layout  # noqa: F401
from .pathway_map import PathwayMap
from .pathway_map_layout import pathway_map_layout  # noqa: F401
from .plot import (  # noqa: F401
    plot_and_save_pathway_graph,
    plot_and_save_pathway_map,
    plot_and_save_sequence_graph,
    plot_pathway_graph,
    plot_pathway_map,
    plot_sequence_graph,
)
from .sequence_graph import SequenceGraph
from .sequence_graph_layout import sequence_graph_layout  # noqa: F401


def sequence_graph_to_pathway_graph(sequence_graph: SequenceGraph) -> PathwayGraph:
    def visit_graph(
        sequence_graph: SequenceGraph,
        pathway_graph: PathwayGraph,
        from_action: Action,
        to_action: Action,
    ) -> None:
        to_action_seen_first = to_action not in pathway_graph._graph.nodes

        pathway_graph.add_conversion(from_action, to_action)

        if to_action_seen_first:
            for to_action_new in sequence_graph.to_actions(to_action):
                visit_graph(sequence_graph, pathway_graph, to_action, to_action_new)

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
