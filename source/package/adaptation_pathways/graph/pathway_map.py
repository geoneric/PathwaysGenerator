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

    def action_begin_by_action(self, action: Action) -> ActionBegin:
        result = None

        for node in self._graph.nodes:
            if isinstance(node, ActionBegin) and node.action == action:
                result = node
                break

        assert result is not None

        return result

    def action_end_by_action(self, action: Action) -> ActionEnd:
        result = None

        for node in self._graph.nodes:
            if isinstance(node, ActionEnd) and node.action == action:
                result = node
                break

        assert result is not None

        return result
