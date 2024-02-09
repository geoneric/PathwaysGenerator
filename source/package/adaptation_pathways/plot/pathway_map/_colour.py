from ...action_combination import ActionCombination
from ...graph.node import ActionBegin, ActionEnd
from ...graph.pathway_map import PathwayMap
from ..colour import (
    PlotColours,
    default_label_colour,
    default_node_edge_colours,
    default_nominal_palette,
    default_transparency,
    nord_palette_dark,
    nord_palette_light,
)


def default_node_colours(
    graph: PathwayMap,
) -> list[tuple[float, float, float, float]]:
    palette = default_nominal_palette()
    colour_by_action_name = colour_by_action_name_pathway_map(graph, palette)
    colours = []

    # Colour each action begin / end combo unique

    for node in graph._graph.nodes:
        assert type(node) in [ActionBegin, ActionEnd]

        action = node.action

        if isinstance(action, ActionCombination):
            colour = nord_palette_light[0] + (default_transparency(),)  # Placeholder
        else:
            colour = colour_by_action_name[action.name]

        colours.append(colour)

    return colours


def colour_by_action_name_pathway_map(
    graph: PathwayMap, palette: list[tuple[float, float, float, float]]
) -> dict[str, tuple[float, float, float, float]]:
    palette_size = len(palette)
    colour_by_action_name = {}
    idx = 0

    for action in graph.actions():
        if not isinstance(action, ActionCombination):
            if action.name not in colour_by_action_name:
                colour_by_action_name[action.name] = palette[idx % palette_size]
                idx += 1

    return colour_by_action_name


def default_edge_colours(
    graph: PathwayMap,
) -> list[tuple[float, float, float, float]]:
    palette = default_nominal_palette()
    colour_by_action_name = colour_by_action_name_pathway_map(graph, palette)
    colours = []

    # Iterate over all edges and use the colour associated with the action associated with the edge
    for from_node, _ in graph._graph.edges:
        if isinstance(from_node, ActionBegin):
            action = from_node.action

            if isinstance(action, ActionCombination):
                colour = nord_palette_dark[0] + (default_transparency(),)  # Placeholder
            else:
                colour = colour_by_action_name[action.name]
        else:
            colour = nord_palette_dark[0] + (
                default_transparency(),
            )  # Default dark colour

        colours.append(colour)

    return colours


def default_colours(pathway_map: PathwayMap) -> PlotColours:
    return PlotColours(
        default_node_colours(pathway_map),
        default_edge_colours(pathway_map),
        default_node_edge_colours(pathway_map),
        default_label_colour(),
    )
