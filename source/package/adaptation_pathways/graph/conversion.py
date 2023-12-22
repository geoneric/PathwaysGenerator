from .node import Action, ActionBegin, ActionEnd
from .pathway_graph import PathwayGraph
from .pathway_map import PathwayMap
from .sequence_graph import SequenceGraph


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
        action,
    ) -> ActionBegin:
        begin = ActionBegin(action)
        end = ActionEnd(action)

        pathway_map.add_period(begin, end)

        for conversion in pathway_graph.to_conversions(action):
            begin_new = visit_graph(
                pathway_graph, pathway_map, pathway_graph.to_action(conversion)
            )
            pathway_map.add_conversion(end, begin_new)

        return begin

    pathway_map = PathwayMap()

    if pathway_graph.nr_nodes() > 0:
        action = pathway_graph.root_node
        visit_graph(pathway_graph, pathway_map, action)

    return pathway_map


def sequence_graph_to_pathway_map(sequence_graph: SequenceGraph) -> PathwayMap:
    return pathway_graph_to_pathway_map(sequence_graph_to_pathway_graph(sequence_graph))
