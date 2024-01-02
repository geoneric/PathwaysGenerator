from .node import Action, ActionBegin, ActionEnd
from .rooted_graph import RootedGraph


class PathwayMap(RootedGraph):
    """
    A PathwayMap represents a collection of adaptation pathways. These pathways are encoded
    in a directed rooted graph in which the nodes represent...
    """

    def add_period(self, begin: ActionBegin, end: ActionEnd) -> None:
        self._graph.add_edge(begin, end)

    def add_conversion(self, end: ActionEnd, begin: ActionBegin) -> None:
        self._graph.add_edge(end, begin)

    def action_begins(self, action_end: ActionEnd) -> list[ActionBegin]:
        assert isinstance(action_end, ActionEnd)
        return list(self._graph.adj[action_end])

    def action_end(self, action_begin: ActionBegin) -> ActionEnd:
        assert isinstance(action_begin, ActionBegin)
        ends = list(self._graph.adj[action_begin])
        assert len(ends) == 1
        return ends[0]

    def all_action_begins_and_ends(
        self, action_begin: ActionBegin
    ) -> list[ActionBegin | ActionEnd]:
        return self.all_to_nodes(action_begin)

    def actions(self) -> set[Action]:
        actions: set[Action] = set()

        for node in self._graph.nodes():
            actions.add(node.action)

        return actions

    def action_begin_by_action(self, action: Action) -> ActionBegin:
        result = None

        for node in self._graph.nodes:
            if isinstance(node, ActionBegin) and node.action == action:
                result = node
                break

        assert result is not None

        return result

    def action_end_by_action(self, action: Action) -> ActionEnd:
        """
        Return ``ActionEnd`` node associated with the action passed in

        :raises LookupError: In case no ``ActionEnd`` node can be found that is associated with
            the action
        """
        result = None

        for node in self._graph.nodes:
            if isinstance(node, ActionEnd) and node.action == action:
                result = node
                break

        if result is None:
            raise LookupError(f"Action {action} is not part of the pathway map")

        return result

    def assign_tipping_points(
        self, tipping_points: dict[Action, int], verify: bool = False
    ) -> None:
        """
        Assign / update tipping points to ActionEnd nodes associated with the actions passed in

        :param verify: Whether or not the tipping points should be checked for consistency,
            using :py:func:`verify_tipping_points`
        """
        for action, tipping_point in tipping_points.items():
            self.action_end_by_action(action).tipping_point = tipping_point

        if verify:
            verify_tipping_points(self)


def verify_tipping_points(pathway_map: PathwayMap) -> None:
    """
    Verify all tipping points in the pathway map passed in are correctly set

    :raises ValueError: In case one or more tipping points are not correctly set

    Tipping points are correct if they strictly increase along the sequences of actions.
    """

    for paths in pathway_map.all_paths():
        # [begin, end, begin, end, ...]

        tipping_point_from = paths[1].tipping_point

        for idx in range(3, len(paths), 2):
            tipping_point_to = paths[idx].tipping_point

            if tipping_point_to <= tipping_point_from:
                raise ValueError(
                    f"Given the sequences of actions, the tipping point of action "
                    f"{paths[idx].action} ({tipping_point_to}) "
                    f"must be at least larger than {tipping_point_from}"
                )

            tipping_point_from = tipping_point_to
