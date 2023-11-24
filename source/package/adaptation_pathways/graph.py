from .actions_graph import ActionsGraph
from .pathways_graph import PathwaysGraph

# from .pathways_map import PathwaysMap
from .sequenced_action import SequencedAction


def visit_actions_graph_edge(
    actions_graph: ActionsGraph, pathways_graph: PathwaysGraph, from_action, to_action
):
    actions_graph_nx = actions_graph.graph
    sequenced_action = SequencedAction(from_action, to_action)

    if actions_graph_nx.in_degree(from_action) == 0:
        pathways_graph.add_action(from_action, sequenced_action)

    if actions_graph_nx.out_degree(to_action) == 0:
        pathways_graph.add_action(sequenced_action, to_action)
    else:
        for to_action_new in actions_graph_nx.adj[to_action]:
            to_sequenced_action = visit_actions_graph_edge(
                actions_graph, pathways_graph, to_action, to_action_new
            )
            pathways_graph.add_action(sequenced_action, to_sequenced_action)

    return sequenced_action


def actions_graph_to_pathways_graph(actions_graph: ActionsGraph) -> PathwaysGraph:
    actions_graph_nx = actions_graph.graph

    # - The root node of the action graph must end up in the pathways graph as the root node
    # - Each leaf node of the actions graph (that is not also a root node) must end up as a
    #   leaf node in the pathways graph
    # - Each edge in the actions graph must end up as a node in the pathways graph

    pathways_graph = PathwaysGraph()

    if not actions_graph.is_empty:
        root_action = actions_graph.root_node

        for to_action in actions_graph_nx.adj[root_action]:
            visit_actions_graph_edge(
                actions_graph, pathways_graph, root_action, to_action
            )

    return pathways_graph


# def pathways_graph_to_pathways_map(pathways_graph: PathwaysGraph) -> PathwaysMap:
#     pathways_map = PathwaysMap()
#
#     return pathways_map
