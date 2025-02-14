from ..action import Action
from ..action_combination import ActionCombination
from .multi_rooted_graph import MultiRootedGraph
from .node import ActionBegin, ActionEnd, TippingPoint


class PathwayMap(MultiRootedGraph):
    """
    A PathwayMap represents a collection of adaptation pathways. These pathways are encoded
    in a directed rooted graph in which the nodes represent...
    """

    def add_period(self, begin: ActionBegin, end: ActionEnd) -> None:
        assert isinstance(begin, ActionBegin)
        assert isinstance(end, ActionEnd)
        self.graph.add_edge(begin, end)

    def add_conversion(self, end: ActionEnd, begin: ActionBegin) -> None:
        assert isinstance(end, ActionEnd)
        assert isinstance(begin, ActionBegin)
        self.graph.add_edge(end, begin)

    def action_begins(self, end: ActionEnd) -> list[ActionBegin]:
        assert isinstance(end, ActionEnd)
        return list(self.graph.adj[end])

    def action_end(self, begin: ActionBegin) -> ActionEnd:
        assert isinstance(begin, ActionBegin)
        ends = list(self.graph.adj[begin])
        assert len(ends) == 1
        return ends[0]

    def all_action_begins_and_ends(
        self, begin: ActionBegin
    ) -> list[ActionBegin | ActionEnd]:
        assert isinstance(begin, ActionBegin)
        return self.all_to_nodes(begin)

    def all_action_begins(self) -> list[ActionBegin]:
        result = []

        for root_node in self.root_nodes:
            assert isinstance(root_node, ActionBegin)

            result.append(root_node)

            for node in self.all_to_nodes(root_node):
                if isinstance(node, ActionBegin):
                    result.append(node)

        return result

    def all_action_ends(self) -> list[ActionEnd]:
        result = []

        for root_node in self.root_nodes:
            assert isinstance(root_node, ActionBegin)

            for node in self.all_to_nodes(root_node):
                if isinstance(node, ActionEnd):
                    result.append(node)

        return result

    def actions(self) -> list[Action]:
        return (
            list(dict.fromkeys(begin.action for begin in self.all_action_begins()))
            if self.nr_nodes() > 0
            else []
        )

    def continued_actions(self, action_combination: ActionCombination) -> list[Action]:
        """
        Return the actions that are continued by the ``action_combination``, if any
        """
        result = []

        # Find node in map containing the action combination passed in

        action_begin: ActionBegin | None = None

        for action_begin in self.all_action_begins():
            if action_begin.action.name == action_combination.name:
                # Current action begin contains the action combination

                for action_end, _ in self.graph.in_edges(action_begin):
                    assert isinstance(action_end, ActionEnd)
                    if action_end.action.name in [
                        action.name for action in action_combination.actions
                    ]:
                        result.append(action_end.action)

        return result

    def action_ends_by_action(self, action: Action) -> list[ActionEnd]:
        """
        Return ``ActionEnd`` nodes associated with the action passed in

        :raises LookupError: In case no ``ActionEnd`` node can be found that is associated with
            the action
        """
        assert isinstance(action, Action), type(action)
        result = []

        for node in self.graph.nodes:
            if isinstance(node, ActionEnd) and node.action == action:
                result.append(node)

        if len(result) == 0:
            raise LookupError(f"Action {action} is not part of the pathway map")

        return result


def verify_tipping_points(
    pathway_map: PathwayMap, tipping_point_by_action: dict[Action, TippingPoint]
) -> None:
    """
    Verify all tipping points in the pathway map passed in are correctly set

    :raises KeyError: In case tipping_point_by_action does not contain tipping points for all actions
    :raises ValueError: In case not all tipping points are strictly increasing along a sequence of actions
    """
    for path in pathway_map.all_paths():
        action_ends = list(path[1::2])
        tipping_points = [
            tipping_point_by_action[action_end.action] for action_end in action_ends
        ]

        if len(action_ends) > 1:
            for tipping_point_idx in range(len(tipping_points) - 1):
                tipping_point_from = tipping_points[tipping_point_idx]
                tipping_point_to = tipping_points[tipping_point_idx + 1]

                if not tipping_point_from < tipping_point_to:
                    raise ValueError(
                        f"Given the sequences of actions, the tipping point of action "
                        f"{action_ends[tipping_point_idx + 1].action} ({tipping_point_to}) "
                        f"must be equal or larger than {tipping_point_from}"
                    )


def tipping_point_range(
    pathway_map: PathwayMap, tipping_point_by_action: dict[Action, TippingPoint]
) -> tuple[TippingPoint, TippingPoint]:
    """
    Return minimum and maximum tipping points
    """
    min_tipping_point = 0.0
    max_tipping_point = 0.0

    if pathway_map.nr_nodes() > 0:
        root_nodes = pathway_map.root_nodes

        # Initialize min tipping point to a value in the actual range of the tipping points
        min_tipping_point = tipping_point_by_action[
            pathway_map.action_end(root_nodes[0]).action
        ]

        for root_node in root_nodes[1:]:
            min_tipping_point = min(
                min_tipping_point,
                tipping_point_by_action[pathway_map.action_end(root_node).action],
            )

        # Initialize max tipping point to a value in the actual range of the tipping points
        max_tipping_point = min_tipping_point

        for end_node in pathway_map.leaf_nodes():
            max_tipping_point = max(
                max_tipping_point, tipping_point_by_action[end_node.action]
            )

    assert (
        min_tipping_point <= max_tipping_point
    ), f"{min_tipping_point} < {max_tipping_point}"

    return min_tipping_point, max_tipping_point
