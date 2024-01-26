from dataclasses import dataclass

from .node import (
    Action,
    ActionBegin,
    ActionCombination,
    ActionConversion,
    ActionEnd,
    ActionPeriod,
)
from .pathway_graph import PathwayGraph
from .pathway_map import PathwayMap
from .sequence_graph import SequenceGraph


@dataclass
class PlotColours:
    node_colours: list[tuple[float, float, float, float]] | None = None
    edge_colours: list[tuple[float, float, float, float]] | None = None
    node_edge_colours: list[tuple[float, float, float, float]] | None = None
    label_colour: tuple[float, float, float, float] | None = None


nord_palette_nominal = [
    (191 / 255, 97 / 255, 106 / 255),  # Redish
    (208 / 255, 135 / 255, 112 / 255),  # Orange
    (235 / 255, 203 / 255, 139 / 255),  # Dark yellow
    (163 / 255, 190 / 255, 140 / 255),  # Green
    (180 / 255, 142 / 255, 173 / 255),  # Purple
]

nord_palette_dark = [
    (46 / 255, 52 / 255, 64 / 255),  # Dark
    (59 / 255, 66 / 255, 82 / 255),  # Lighter than nord0
    (67 / 255, 76 / 255, 94 / 255),  # Lighter than nord1
    (76 / 255, 86 / 255, 106 / 255),  # Lighter than nord2
]

nord_palette_light = [
    (216 / 255, 222 / 255, 233 / 255),  # Bright
    (229 / 255, 233 / 255, 240 / 255),  # Lighter than nord4
    (236 / 255, 239 / 255, 244 / 255),  # Lighter than nord5
]

nord_palette_blue = [
    (143 / 255, 188 / 255, 187 / 255),  # Calm, frozen polar water
    (136 / 255, 192 / 255, 208 / 255),  # Bright, shiny, pure and clear ice
    (129 / 255, 161 / 255, 193 / 255),  # Darkened, arctic waters
    (94 / 255, 129 / 255, 172 / 255),  # Dark, deep arctic ocean
]


def default_transparency():
    return 1.0  # 0.75


def default_nominal_palette() -> list[tuple[float, float, float, float]]:
    palette = [colour + (default_transparency(),) for colour in nord_palette_nominal]
    palette.append(nord_palette_blue[0] + (default_transparency(),))

    return palette


def default_node_colours_sequence_graph(
    graph: SequenceGraph,
) -> list[tuple[float, float, float, float]]:
    palette = default_nominal_palette()

    palette_size = len(palette)
    colour_by_action = {}
    colours = []

    # Colour each unique action unique
    idx = 0

    for node in graph._graph.nodes:
        assert isinstance(node, Action)
        if node not in colour_by_action:
            colour_by_action[node] = palette[idx % palette_size]
            idx += 1
        colours.append(colour_by_action[node])

    return colours


def default_node_colours_pathway_graph(
    graph: PathwayGraph,
) -> list[tuple[float, float, float, float]]:
    palette = default_nominal_palette()

    palette_size = len(palette)
    conversion_colour = nord_palette_light[0] + (default_transparency(),)

    colour_by_action = {}
    colours = []

    # Use the same colour for conversions
    # Colour each unique action unique
    idx = 0

    for node in graph._graph.nodes:
        # assert type(node) in [Action, ActionConversion]
        assert type(node) in [ActionConversion, ActionPeriod]
        if isinstance(node, ActionPeriod):
            if node not in colour_by_action:
                colour_by_action[node] = palette[idx % palette_size]
                idx += 1
            colours.append(colour_by_action[node])
        elif isinstance(node, ActionConversion):
            colours.append(conversion_colour)

    return colours


def colour_by_action_pathway_map(
    graph: PathwayMap, palette: list[tuple[float, float, float, float]]
) -> dict[Action, tuple[float, float, float, float]]:
    palette_size = len(palette)
    colour_by_action = {}
    idx = 0

    for action in graph.actions():
        if not isinstance(action, ActionCombination):
            if action not in colour_by_action:
                colour_by_action[action] = palette[idx % palette_size]
                idx += 1

    return colour_by_action


def default_node_colours_pathway_map(
    graph: PathwayMap,
) -> list[tuple[float, float, float, float]]:
    palette = default_nominal_palette()
    colour_by_action = colour_by_action_pathway_map(graph, palette)
    colours = []

    # Colour each action begin / end combo unique

    for node in graph._graph.nodes:
        assert type(node) in [ActionBegin, ActionEnd]

        action = node.action

        if isinstance(action, ActionCombination):
            colour = nord_palette_light[0] + (default_transparency(),)  # Placeholder
        else:
            colour = colour_by_action[action]

        colours.append(colour)

    return colours


def default_edge_colours(
    graph: SequenceGraph | PathwayGraph,
) -> list[tuple[float, float, float, float]]:
    colour = nord_palette_dark[3] + (default_transparency(),)
    colours = [colour] * len(list(graph.graph.edges))

    return colours


def default_edge_colours_pathway_map(
    graph: PathwayMap,
) -> list[tuple[float, float, float, float]]:
    palette = default_nominal_palette()
    colour_by_action = colour_by_action_pathway_map(graph, palette)
    colours = []

    # Iterate over all edges and use the colour associated with the action associated with the edge
    for from_node, _ in graph._graph.edges:
        if isinstance(from_node, ActionBegin):
            action = from_node.action

            if isinstance(action, ActionCombination):
                colour = nord_palette_dark[0] + (default_transparency(),)  # Placeholder
            else:
                colour = colour_by_action[action]
        else:
            colour = nord_palette_dark[0] + (
                default_transparency(),
            )  # Default dark colour

        colours.append(colour)

    return colours


def default_node_edge_colours(
    graph: SequenceGraph | PathwayGraph | PathwayMap,
) -> list[tuple[float, float, float, float]]:
    colour = nord_palette_dark[3] + (default_transparency(),)
    colours = [colour] * len(list(graph.graph.edges))

    return colours


def default_label_colour() -> tuple[float, float, float, float]:
    return nord_palette_dark[0] + (default_transparency(),)


def default_sequence_graph_colours(sequence_graph: SequenceGraph) -> PlotColours:
    return PlotColours(
        default_node_colours_sequence_graph(sequence_graph),
        default_edge_colours(sequence_graph),
        default_node_edge_colours(sequence_graph),
        default_label_colour(),
    )


def default_pathway_graph_colours(pathway_graph: PathwayGraph) -> PlotColours:
    return PlotColours(
        default_node_colours_pathway_graph(pathway_graph),
        default_edge_colours(pathway_graph),
        default_node_edge_colours(pathway_graph),
        default_label_colour(),
    )


def default_pathway_map_colours(pathway_map: PathwayMap) -> PlotColours:
    return PlotColours(
        default_node_colours_pathway_map(pathway_map),
        default_edge_colours_pathway_map(pathway_map),
        default_node_edge_colours(pathway_map),
        default_label_colour(),
    )
