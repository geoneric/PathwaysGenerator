from ..action import Action
from ..action_conversion import ActionConversion
from .rooted_graph import RootedGraph


class PathwayGraph(RootedGraph):
    """
    A PathwayGraph represents the dependencies between action sequences. The nodes represent
    the conversion from one action to another (think tipping points or vertical lines in a
    pathway map), and the edges the period of time a certain action is active (think horizontal
    lines in a pathway map).
    """

    def start_pathway(
        self, from_action: Action, to_conversion: ActionConversion
    ) -> None:
        """
        Add a period, defined by an action and a conversions
        """
        self._graph.add_edge(from_action, to_conversion)

    def add_conversion(self, from_action: Action, to_action: Action) -> None:
        """
        Add a conversion, defined by two actions
        """
        conversion = ActionConversion(from_action, to_action)
        self._graph.add_edge(from_action, conversion)
        self._graph.add_edge(conversion, to_action)

    def end_pathway(self, from_conversion: ActionConversion, to_action: Action) -> None:
        """
        Add a period, defined by a conversion and an action
        """
        self._graph.add_edge(from_conversion, to_action)

    def set_pathway(self, from_action: Action, to_action: Action) -> None:
        """
        Add a pathway, defined by a single period defined by two actions
        """
        self._graph.add_edge(from_action, to_action)

    def nr_conversions(self) -> int:
        """
        :return: Number of conversions, including the start and end actions of pathways
        """
        return self.nr_nodes()

    def nr_to_conversions(self, from_conversion: ActionConversion | Action) -> int:
        return self._graph.out_degree(from_conversion)

    def to_conversions(
        self, from_conversion: ActionConversion | Action
    ) -> list[ActionConversion]:
        return list(self._graph.adj[from_conversion])

    def to_action(self, conversion: ActionConversion) -> Action:
        actions = list(self._graph.adj[conversion])
        assert len(actions) == 1
        return actions[0]

    def conversion_by_name(self, name: str) -> ActionConversion | Action:
        result = None

        for node in self._graph.nodes:
            if node.label == name:
                result = node
                break

        assert result is not None

        return result

    def all_to_actions_and_conversions(
        self, from_action: Action
    ) -> list[Action | ActionConversion]:
        return self.all_to_nodes(from_action)
