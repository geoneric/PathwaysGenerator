from ...graph import SequenceGraph
from ...graph.node import Action as ActionNode
from .. import alias
from ..colour import (
    PlotColours,
    default_edge_colours,
    default_edge_style,
    default_label_colour,
    default_node_edge_colours,
    default_node_style,
)


def colour_by_node(
    graph: SequenceGraph, colour_by_action_name: dict[str, alias.Colour]
) -> list[alias.Colour | alias.Colours]:
    # pylint: disable=redefined-outer-name
    colours: list[alias.Colour | alias.Colours] = []

    for node in graph._graph.nodes:
        assert isinstance(node, ActionNode)
        assert node.action.name in colour_by_action_name, node.action
        colours.append(colour_by_action_name[node.action.name])

    return colours


def colour_by_action_name_sequence_graph(
    graph: SequenceGraph, palette: alias.Colours
) -> dict[str, alias.Colour]:
    palette_size = len(palette)
    result = {}

    idx = 0

    for node in graph._graph.nodes:
        assert isinstance(node, ActionNode)
        if node.action.name not in result:
            result[node.action.name] = palette[idx % palette_size]
            idx += 1

    return result


def default_colours(
    sequence_graph: SequenceGraph, colour_by_action_name: dict[str, alias.Colour]
) -> PlotColours:
    return PlotColours(
        colour_by_node(sequence_graph, colour_by_action_name),
        default_node_style(),
        default_edge_colours(sequence_graph),
        default_edge_style(),
        default_node_edge_colours(sequence_graph),
        default_label_colour(),
    )
