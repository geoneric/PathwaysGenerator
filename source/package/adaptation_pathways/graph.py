from .actions_graph import ActionsGraph
from .pathways_graph import PathwaysGraph
from .sequenced_action import SequencedAction


def actions_graph_to_pathways_graph(actions_graph: ActionsGraph) -> PathwaysGraph:
    pathways_graph = PathwaysGraph()
    sequenced_actions = []

    # Each edge in the actions graph represents a relation between two actions. A pathways
    # graph contains the relations between these relations. Therefore, each edge in the actions
    # graph ends up as a node in the pathways graph.
    for from_action, to_action in actions_graph.graph.edges:
        # Think "vertical lines in the pathways map"
        action = SequencedAction(from_action, to_action)
        pathways_graph.add_sequence(action)
        sequenced_actions.append(action)

    # Each node in the actions graph becomes an edge in the pathways graph
    for action in actions_graph.graph.nodes:
        # Think "horizontal lines in the pathways map"
        # Link sequences that end with this action with sequences that start with this action
        to_actions = [
            action_ for action_ in sequenced_actions if action_.to_action == action
        ]
        from_actions = [
            action_ for action_ in sequenced_actions if action_.from_action == action
        ]

        for to_action in to_actions:
            if from_actions:
                for from_action in from_actions:
                    # pylint: disable-next=arguments-out-of-order
                    pathways_graph.add_action(to_action, from_action)
            else:
                # Actions for which there is not follow-up action (to_action), are the terminals in
                # the pathway map. We can end them with the action itself.
                pathways_graph.add_action(to_action, action)

    # Now we have a graph that corresponds more with the pathways map used to visualize pathways

    return pathways_graph
