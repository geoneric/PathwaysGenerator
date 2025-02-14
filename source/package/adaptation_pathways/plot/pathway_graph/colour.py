from ...graph import PathwayGraph
from ...graph.node import ActionConversion, ActionPeriod
from .. import alias
from ..colour import (
    PlotColours,
    default_edge_colours,
    default_edge_style,
    default_label_colour,
    default_node_edge_colours,
    default_node_style,
    nord_palette_light,
)


def colour_by_node(
    graph: PathwayGraph, colour_by_action_name: dict[str, alias.Colour]
) -> list[alias.Colour | alias.Colours]:
    # pylint: disable=redefined-outer-name
    colours: list[alias.Colour | alias.Colours] = []
    conversion_colour = nord_palette_light[0]

    # Use the same colour for conversions
    # Colour each unique action unique
    for node in graph._graph.nodes:
        assert type(node) in [ActionConversion, ActionPeriod]
        if isinstance(node, ActionPeriod):
            colours.append(colour_by_action_name[node.action.name])
        elif isinstance(node, ActionConversion):
            colours.append(conversion_colour)

    return colours


def colour_by_action_name_pathway_graph(
    graph: PathwayGraph, palette: alias.Colours
) -> dict[str, alias.Colour]:
    palette_size = len(palette)
    result = {}
    idx = 0

    for node in graph._graph.nodes:
        assert type(node) in [ActionConversion, ActionPeriod]
        if isinstance(node, ActionPeriod):
            if node.action.name not in result:
                result[node.action.name] = palette[idx % palette_size]
                idx += 1

    return result


def default_colours(
    pathway_graph: PathwayGraph, colour_by_action_name: dict[str, alias.Colour]
) -> PlotColours:
    return PlotColours(
        colour_by_node(pathway_graph, colour_by_action_name),
        default_node_style(),
        default_edge_colours(pathway_graph),
        default_edge_style(),
        default_node_edge_colours(pathway_graph),
        default_label_colour(),
    )
