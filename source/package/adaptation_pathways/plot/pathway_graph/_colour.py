from ...graph.node import ActionConversion, ActionPeriod
from ...graph.pathway_graph import PathwayGraph
from ..colour import (
    Colours,
    PlotColours,
    default_edge_colours,
    default_label_colour,
    default_node_edge_colours,
    default_nominal_palette,
    default_transparency,
    nord_palette_light,
)


def default_node_colours(graph: PathwayGraph) -> Colours:
    palette = default_nominal_palette()

    palette_size = len(palette)
    conversion_colour = nord_palette_light[0] + (default_transparency(),)

    colour_by_action_name = {}
    colours = []

    # Use the same colour for conversions
    # Colour each unique action unique
    idx = 0

    for node in graph._graph.nodes:
        # assert type(node) in [Action, ActionConversion]
        assert type(node) in [ActionConversion, ActionPeriod]
        if isinstance(node, ActionPeriod):
            if node.action.name not in colour_by_action_name:
                colour_by_action_name[node.action.name] = palette[idx % palette_size]
                idx += 1
            colours.append(colour_by_action_name[node.action.name])
        elif isinstance(node, ActionConversion):
            colours.append(conversion_colour)

    return colours


def default_colours(pathway_graph: PathwayGraph) -> PlotColours:
    return PlotColours(
        default_node_colours(pathway_graph),
        default_edge_colours(pathway_graph),
        default_node_edge_colours(pathway_graph),
        default_label_colour(),
    )
