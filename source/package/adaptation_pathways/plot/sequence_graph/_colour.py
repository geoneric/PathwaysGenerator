from ...graph.node import Action as ActionNode
from ...graph.sequence_graph import SequenceGraph
from ..colour import (
    PlotColours,
    default_edge_colours,
    default_label_colour,
    default_node_edge_colours,
    default_nominal_palette,
)


def default_node_colours(
    graph: SequenceGraph,
) -> list[tuple[float, float, float, float]]:
    palette = default_nominal_palette()

    palette_size = len(palette)
    colour_by_action_name = {}
    colours = []

    # Colour each unique action unique
    idx = 0

    for node in graph._graph.nodes:
        assert isinstance(node, ActionNode)
        if node.action.name not in colour_by_action_name:
            colour_by_action_name[node.action.name] = palette[idx % palette_size]
            idx += 1
        colours.append(colour_by_action_name[node.action.name])

    return colours


def default_colours(sequence_graph: SequenceGraph) -> PlotColours:
    return PlotColours(
        default_node_colours(sequence_graph),
        default_edge_colours(sequence_graph),
        default_node_edge_colours(sequence_graph),
        default_label_colour(),
    )
